# meraki-exporter 🚀

A production-ready Python automation script to export and back up your entire Cisco Meraki infrastructure using the Meraki Dashboard API.

Stop clicking "Export to CSV" on dozens of individual dashboard pages. This tool programmatically extracts your network configurations, organization settings, wireless profiles, switch matrices, and hardware telemetry into a single, comprehensive, timestamped JSON backup file with zero manual intervention.

## ✨ Features
* **Zero-Touch Execution:** Interactive, masked API credential input keeps your workspace clean and secure.
* **Full-Tenant Mapping:** Recursively iterates through all accessible Organizations, Networks, and managed devices.
* **Granular Asset Telemetry:** Captures full switch-port matrices (MS Series) and active antenna/radio calibrations (MR Series).
* **Failsafe API Handling:** Gracefully handles segments missing explicit licenses (e.g., skipping wireless queries safely on non-wireless networks) without crashing the runtime.
* **Post-Run Sanity Audit:** Prints a complete cryptographic/logical summary report upon successful execution to verify captured datasets.
* **Strictly Read-Only:** Built entirely using `GET` requests—guaranteeing zero risk to your live production environment.

## 🛠️ Prerequisites
Before running the script, ensure you have the following:
* **Python 3.8+**
* An active Cisco Meraki **API Key** (Generated via the Meraki Dashboard under *My Profile*).
* Dashboard API Access enabled for your organization (*Organization > Settings > Dashboard API Access*).

## 📥 1. Clone the Repository
Run the following commands in your terminal to download the project files and step into the directory:

    git clone https://github.com/YOUR_USERNAME/meraki-exporter.git
    cd meraki-exporter

## ⚙️ 2. Install Dependencies
Install the official Cisco Meraki Python SDK to your environment before running the tool:

    pip install meraki

## 🚀 3. Run the Script
Execute the script. You will be securely prompted to input your API token (the input characters will be completely hidden for security):

    python meraki-archive-script-via-api.py

## 📂 4. Output Manifest
Once execution completes, the script generates a standalone, timestamped data matrix in the root directory:

    .
    ├── meraki-archive-script-via-api.py
    └── meraki_safe_backup_YYYYMMDD_HHMMSS.json  <-- Complete Infrastructure Backup

## 🔒 Security Best Practices
* **Runtime Masking:** This script leverages Python's native `getpass` library to ensure your API token never touches hardcoded plain text, standard output streams, or local shell histories.
* **Least Privilege:** For standard drift mitigation and backup baselines, it is highly recommended to pair this tool with a read-only administrator API profile.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to open a ticket on the issues page.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
