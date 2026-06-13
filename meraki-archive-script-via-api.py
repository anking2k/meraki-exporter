import json
import os
import getpass
from datetime import datetime
import meraki

def run_readonly_backup():
    # 1. Secure Runtime Authentication (Input is completely masked)
    api_key = getpass.getpass("🔑 Enter your Meraki API Key: ").strip()
    
    if not api_key:
        print("❌ Action aborted: API Key cannot be blank.")
        return

    print("\n[INIT] Initializing Read-Only Meraki Dashboard Session...")
    # Instantiate the dashboard. Native logging is suppressed to keep output clean.
    dashboard = meraki.DashboardAPI(api_key, suppress_logging=True)

    # Counters for the post-run execution check
    stats = {
        "orgs_processed": 0,
        "networks_processed": 0,
        "total_ssids_captured": 0,
        "total_rf_profiles_captured": 0,
        "total_switches_inventoried": 0,
        "total_switch_ports_captured": 0,
        "total_aps_inventoried": 0,
        "total_ap_radios_captured": 0
    }

    backup_data = {
        "backup_metadata": {
            "timestamp": datetime.now().isoformat(),
            "script_version": "1.0.0",
            "execution_mode": "STRICT_READ_ONLY_GET"
        },
        "organizations": []
    }

    try:
        # 2. Pull accessible Organizations
        print("[GET] Fetching account-accessible Organizations...")
        organizations = dashboard.organizations.getOrganizations()

        for org in organizations:
            org_id = org['id']
            org_name = org['name']
            stats["orgs_processed"] += 1
            print(f"\n🏢 Processing Org: {org_name} ({org_id})")
            
            org_data = {
                "org_info": org,
                "networks": []
            }

            # 3. Pull Networks mapping out the Org
            networks = dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')
            
            for net in networks:
                net_id = net['id']
                net_name = net['name']
                stats["networks_processed"] += 1
                print(f"  └── 🌐 Network: {net_name}")

                net_data = {
                    "network_info": net,
                    "global_wireless_settings": {},
                    "wireless_ssids": [],
                    "wireless_rf_profiles": [],
                    "devices": []
                }

                # 4. Pull Macro Wireless Configurations (SSID/RF Plans)
                if 'wireless' in net.get('productTypes', []):
                    try:
                        print(f"      ├── [GET] Global Wireless Parameters...")
                        net_data["global_wireless_settings"] = dashboard.wireless.getNetworkWirelessSettings(net_id)
                        
                        print(f"      ├── [GET] Broadcasted SSIDs Profiles...")
                        ssids = dashboard.wireless.getNetworkWirelessSsids(net_id)
                        net_data["wireless_ssids"] = ssids
                        stats["total_ssids_captured"] += len(ssids)
                        
                        print(f"      ├── [GET] RF Profiles & Channel Plans...")
                        rf_prof = dashboard.wireless.getNetworkWirelessRfProfiles(net_id)
                        net_data["wireless_rf_profiles"] = rf_prof
                        stats["total_rf_profiles_captured"] += len(rf_prof)
                    except meraki.APIError as e:
                        print(f"      ⚠️ Skipping wireless pull for this segment: {e.message}")

                # 5. Inventory Devices & Extract Granular Port/Radio Maps
                print(f"      ├── [GET] Fetching device asset inventory...")
                devices = dashboard.networks.getNetworkDevices(net_id)
                
                for device in devices:
                    serial = device['serial']
                    product_type = device.get('productType')
                    model = device.get('model', '')
                    device_name = device.get('name', serial)

                    # --- TARGET SWITCHES (MS Series) ---
                    if product_type == 'switch' or 'MS' in model:
                        stats["total_switches_inventoried"] += 1
                        print(f"      │   └── 🔌 Pulling port matrix for Switch: {device_name}")
                        try:
                            ports = dashboard.switch.getDeviceSwitchPorts(serial)
                            device['port_configurations'] = ports
                            stats["total_switch_ports_captured"] += len(ports)
                        except meraki.APIError as e:
                            print(f"      │       ⚠️ Ports extraction failed for {serial}: {e.message}")
                            device['port_configurations'] = []

                    # --- TARGET ACCESS POINTS (MR Series) ---
                    elif product_type == 'wireless' or 'MR' in model:
                        stats["total_aps_inventoried"] += 1
                        print(f"      │   └── 📶 Pulling antenna profiles for AP: {device_name}")
                        try:
                            radios = dashboard.wireless.getDeviceWirelessRadioSettings(serial)
                            device['radio_settings'] = radios
                            stats["total_ap_radios_captured"] += 1
                        except meraki.APIError as e:
                            print(f"      │       ⚠️ Radio profiling failed for {serial}: {e.message}")
                            device['radio_settings'] = {}

                    net_data["devices"].append(device)

                org_data["networks"].append(net_data)
            
            backup_data["organizations"].append(org_data)

        # 6. Stream compiled data to a timestamped JSON file
        filename = f"meraki_safe_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=4)
        
        # 7. Print the Final Audit Report
        print_sanity_report(stats, filename)

    except meraki.APIError as e:
        print(f"\n❌ Meraki API Gateway Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected System Error: {e}")

def print_sanity_report(stats, file_path):
    print("\n" + "="*50)
    print("📋 POST-RUN Q/A SANITY CHECK REPORT")
    print("="*50)
    print(f"🔒 EXECUTION MODE        : STRICTLY READ-ONLY (GET)")
    print(f"💾 BACKUP FILE DESTINATION: {os.path.abspath(file_path)}")
    print("-"*50)
    print(f"🏢 Organizations Scanned : {stats['orgs_processed']}")
    print(f"🌐 Total Networks Map     : {stats['networks_processed']}")
    print(f"📡 SSIDs Documented       : {stats['total_ssids_captured']}")
    print(f"📊 RF Layout Profiles     : {stats['total_rf_profiles_captured']}")
    print("-"*50)
    print(f"🔌 Total Switches Logged  : {stats['total_switches_inventoried']} units")
    print(f"🎛️  Switch Ports Configured  : {stats['total_switch_ports_captured']} ports mapped")
    print(f"📶 APs Managed           : {stats['total_aps_inventoried']} units")
    print(f"📻 AP Radios Calibrated   : {stats['total_ap_radios_captured']} hardware radios logged")
    print("="*50)
    print("🛡️  SAFETY ASSERTION: Zero configuration state changes were pushed.")
    print("   Only read-only data extraction loops were performed.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_readonly_backup()