# Tithing Dashboard 2026 [CYBER-LINK v1.0]

A sleek, cyberpunk-themed financial ledger built with Python and CustomTkinter, designed to track monthly income and automate tithe calculations with precision.

## ⚡ Features

- **Cyber-Link UI**: High-contrast, dark-mode interface with neon crimson and cyan accents.
- **Monthly Data Streams**: Dedicated segments for every month to track individual income entries.
- **Transaction Injection**: Easy input for financial transactions with automated timestamps.
- **Automated Tithe Engine**: Calculates the 10% tithe goal automatically, with rounding logic to ensure commitments are met.
- **Data Persistence**: All records are stored locally in a secure `tithing_data.json` file.
- **Purge Functionality**: Ability to remove individual entries from the transaction log.

## 🛠 Tech Stack

- **Language**: Python 3.10+
- **UI Framework**: CustomTkinter
- **Persistence**: JSON

## 🚀 Getting Started

1. **Install Dependencies**:
   Ensure you have Python installed, then install the required UI library:
   ```bash
   pip install customtkinter
   ```

2. **Run the Application**:
   Execute the main script to launch the dashboard:
   ```bash
   python tithing.py
   ```

## 📂 Project Structure

- `tithing.py`: The core application logic and UI controller.
- `tithing_data.json`: Local data store (created on first run).
- `.gitignore`: Standard exclusions for Python projects and local data.

---
*System Version: CYBER-LINK v1.0*