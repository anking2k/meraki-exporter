# meraki-exporter 🚀

A production-ready Python automation script to flawlessly export and back up your entire Cisco Meraki infrastructure using the Meraki Dashboard API.

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

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/meraki-exporter.git](https://github.com/YOUR_USERNAME/meraki-exporter.git)
cd meraki-exporter
