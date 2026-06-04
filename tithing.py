import os
import json
import math
from datetime import datetime
import customtkinter as ctk

# --- DATA MANIFEST & PERSISTENCE CONFIG ---
DATA_FILE = "tithing_data.json"
MONTHS = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

# --- APPLICATION CONTROLLER ---
class TithingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Tithing Dashboard 2026 [CYBER-LINK v1.0]") # Main Window Title
        self.geometry("780x850")
        
        # Core Cyberpunk Theme Enforcement
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#0d0e12") # Deep obsidian backdrop override

        # State Variables
        self.records = {
            month: {"incomeEntries": [], "amountPaid": "0", "lastPaidDate": ""}
            for month in MONTHS
        }
        self.running_total = 0.0
        self.selected_month = MONTHS[0]
        
        # Load Existing Safe State
        self.load_data()

        # Build Container Shell
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=25, pady=25)

        # Show Core Ledger Segment First
        self.show_dashboard_view()

    # --- CALCULATION LOGIC ---
    def get_total_income(self, month):
        return sum(entry["amount"] for entry in self.records[month]["incomeEntries"])

    def get_tithe_goal(self, month):
        return self.get_total_income(month) * 0.1

    def get_tithe_goal_rounded(self, month):
        return math.ceil(self.get_tithe_goal(month))

    def recalculate_total(self):
        self.running_total = 0.0
        for month in MONTHS:
            exact_tithe = self.get_tithe_goal(month)
            if exact_tithe > 0:
                self.running_total += math.ceil(exact_tithe)

    # --- JSON DISK INTERFACE ---
    def save_data(self):
        payload = {
            "records": self.records,
            "runningTotal": self.running_total
        }
        with open(DATA_FILE, "w") as f:
            json.dump(payload, f, indent=2)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.records = data.get("records", self.records)
                    self.recalculate_total()
            except Exception as e:
                print(f"Failed to read data stream: {e}")

    # --- VIEW SWAPPING CONTROLLER ---
    def clear_view(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- 1. SYSTEM OVERVIEW // CORE LEDGER ---
    def show_dashboard_view(self):
        self.clear_view()

        # Main Dashboard Heading
        title_lbl = ctk.CTkLabel(
            self.main_container, 
            text="Yearly Overview", # Section Header
            font=("Segoe UI", 24, "bold"),
            text_color="#f0f2f5"
        )
        title_lbl.pack(anchor="center", pady=(0, 2))

        total_lbl = ctk.CTkLabel(
            self.main_container, 
            text=f"Total Contributions (Rounded): ${self.running_total:,.2f}", # Aggregated UI display
            font=("Segoe UI", 18, "bold"),
            text_color="#ff2e54" # Neon Crimson
        )
        total_lbl.pack(anchor="center", pady=(0, 15))

        # Horizontal Rule
        sep = ctk.CTkFrame(self.main_container, height=2, fg_color="#2a2f3d")
        sep.pack(fill="x", pady=(0, 20))

        # 4x3 Grid Framework for Month Cards
        grid_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        for idx, month in enumerate(MONTHS):
            row = idx // 3
            col = idx % 3

            # Dark grey card container
            card = ctk.CTkFrame(grid_frame, fg_color="#161920", border_color="#2a2f3d", border_width=1, corner_radius=8)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            lbl_month = ctk.CTkLabel(card, text=month, font=("Segoe UI", 16, "bold"), text_color="#ffffff") # Month identifier
            lbl_month.pack(anchor="w", padx=12, pady=(12, 2))

            target_val = self.get_tithe_goal_rounded(month)
            lbl_target = ctk.CTkLabel(card, text=f"Tithe: ${target_val}", font=("Segoe UI", 13, "bold"), text_color="#ff3366") # Calculated target
            lbl_target.pack(anchor="w", padx=12, pady=(0, 10))

            # Access Action Button
            btn = ctk.CTkButton(
                card, 
                text="Access Segment", # Navigation button text
                fg_color="transparent",
                text_color="#00f2fe", # Cyan Interactive Elements
                hover_color="#1c212b",
                font=("Segoe UI", 13, "bold"),
                command=lambda m=month: self.show_month_detail_view(m)
            )
            btn.pack(fill="x", padx=12, pady=(0, 12))

    # --- 2. MONTH DATA STREAM DETAIL VIEW ---
    def show_month_detail_view(self, month):
        self.selected_month = month
        self.clear_view()

        title_lbl = ctk.CTkLabel(
            self.main_container, 
            text=f"{month} Data Stream", # Sub-view header indicating current data context
            font=("Segoe UI", 26, "bold"),
            text_color="#f0f2f5"
        )
        title_lbl.pack(pady=(0, 15))

        # Dark Central Panel
        pane = ctk.CTkFrame(self.main_container, fg_color="#161920", border_color="#2a2f3d", border_width=1, corner_radius=8)
        pane.pack(fill="both", expand=True, padx=10, pady=10)

        # Transaction Insertion Block
        input_frame = ctk.CTkFrame(pane, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=15)

        lbl_prompt = ctk.CTkLabel(input_frame, text="Input Transaction Value ($):", font=("Segoe UI", 13), text_color="#c9d1d9") # Entry prompt
        lbl_prompt.pack(anchor="w", pady=(0, 5))

        # Horizontal Row layout container for Entry + Button
        row_entry_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        row_entry_frame.pack(fill="x")

        entry_val = ctk.CTkEntry(row_entry_frame, fg_color="#0d0e12", border_color="#2a2f3d", text_color="#ffffff")
        entry_val.pack(side="left", fill="x", expand=True, padx=(0, 10))

        def inject_entry():
            try:
                val = float(entry_val.get())
                if val > 0:
                    timestamp = datetime.now().strftime("%m/%d")
                    self.records[month]["incomeEntries"].append({"amount": val, "dateStr": timestamp})
                    self.recalculate_total()
                    self.save_data()
                    self.show_month_detail_view(month)
            except ValueError:
                pass

        btn_inject = ctk.CTkButton(
            row_entry_frame, 
            text="Inject Entry", # Submission button text
            fg_color="#005f73", 
            text_color="#00f2fe", 
            border_color="#00f2fe",
            border_width=1,
            hover_color="#00f2fe",
            font=("Segoe UI", 13, "bold"),
            command=inject_entry
        )
        btn_inject.pack(side="right")

        # Dynamic History Log List Box
        scroll_frame = ctk.CTkScrollableFrame(pane, fg_color="#0d0e12", border_color="#2a2f3d", border_width=1, height=220)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        lbl_hist_title = ctk.CTkLabel(scroll_frame, text="Transaction History Log", font=("Segoe UI", 14, "bold"), text_color="#ffffff") # List title
        lbl_hist_title.pack(anchor="w", padx=5, pady=5)

        for idx, entry in enumerate(self.records[month]["incomeEntries"]):
            row_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)

            log_lbl = ctk.CTkLabel(
                row_frame, 
                text=f"• [{entry['dateStr']}]  ${entry['amount']:,.2f}", # Formatted history entry
                font=("Segoe UI", 13), 
                text_color="#c9d1d9"
            )
            log_lbl.pack(side="left", padx=5)

            # Creating an isolated scope callback to ensure correct item index deletion
            def make_delete_cmd(target_idx=idx):
                return lambda: [
                    self.records[month]["incomeEntries"].pop(target_idx),
                    self.recalculate_total(),
                    self.save_data(),
                    self.show_month_detail_view(month)
                ]

            btn_purge = ctk.CTkButton(
                row_frame, 
                text="Purge", # Item deletion button text
                width=60,
                height=24,
                fg_color="#2c161a", 
                text_color="#ff5555", 
                border_color="#ff5555",
                border_width=1,
                hover_color="#ff5555",
                font=("Segoe UI", 11, "bold"),
                command=make_delete_cmd(idx)
            )
            btn_purge.pack(side="right", padx=5)

        # Metrics Breakout Footnotes
        metrics_frame = ctk.CTkFrame(pane, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=20, pady=15)

        gross_vol = self.get_total_income(month)
        lbl_gross = ctk.CTkLabel(metrics_frame, text=f"Total Income: ${gross_vol:,.2f}", font=("Segoe UI", 14, "bold"), text_color="#ffffff") # Total calculated income
        lbl_gross.pack(anchor="w")

        calc_rate = self.get_tithe_goal(month)
        lbl_rate = ctk.CTkLabel(metrics_frame, text=f"Calculated Rate (10%): ${calc_rate:,.2f}", font=("Segoe UI", 13, "italic"), text_color="#8b949e") # Precise decimal value
        lbl_rate.pack(anchor="w")

        target_alloc = self.get_tithe_goal_rounded(month)
        lbl_alloc = ctk.CTkLabel(metrics_frame, text=f"Rounded Tithe: ${target_alloc}", font=("Segoe UI", 15, "bold"), text_color="#ff2e54") # Final rounded requirement
        lbl_alloc.pack(anchor="w", pady=(0, 5))

        if self.records[month]["lastPaidDate"]:
            lbl_commit = ctk.CTkLabel(metrics_frame, text=f"Date Saved: {self.records[month]['lastPaidDate']}", font=("Segoe UI", 12, "italic"), text_color="#8b949e") # Last save timestamp
            lbl_commit.pack(anchor="w")

        # Bottom Command Operations Bar
        def commit_metrics():
            self.records[month]["amountPaid"] = str(self.get_tithe_goal_rounded(month))
            self.records[month]["lastPaidDate"] = datetime.now().strftime("%Y-%m-%d")
            self.recalculate_total()
            self.save_data()
            self.show_dashboard_view()

        btn_commit = ctk.CTkButton(
            pane, 
            text="Commit Metrics", # Save and close button text
            fg_color="#005f73", 
            text_color="#00f2fe", 
            border_color="#00f2fe",
            border_width=1,
            hover_color="#00f2fe",
            font=("Segoe UI", 14, "bold"),
            command=commit_metrics
        )
        btn_commit.pack(fill="x", padx=20, pady=(10, 5))

        btn_back = ctk.CTkButton(
            pane, 
            text="← Main Menu", # Return navigation text
            width=100,
            fg_color="#0d0e12", 
            text_color="#8b949e", 
            border_color="#2a2f3d",
            border_width=1,
            hover_color="#161920",
            font=("Segoe UI", 12),
            command=self.show_dashboard_view
        )
        btn_back.pack(anchor="w", padx=20, pady=(0, 15))


# --- RUN ENGINE ---
if __name__ == "__main__":
    app = TithingApp()
    app.mainloop()