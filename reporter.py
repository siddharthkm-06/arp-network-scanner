import json
import os
from datetime import datetime
from vendor import get_vendor

RESULTS_FOLDER = "results"


def display_table(devices):
    """
    Prints a formatted table of all discovered devices.
    """
    print("\n" + "=" * 65)
    print(f"  {'IP Address':<18} {'MAC Address':<20} {'Vendor'}")
    print(f"  {'-'*17:<18} {'-'*19:<20} {'-'*20}")

    for device in devices:
        ip = device["ip"]
        mac = device["mac"]
        vendor = device.get("vendor", "Unknown")
        print(f"  {ip:<18} {mac:<20} {vendor}")

    print("=" * 65)
    print(f"  Total devices found: {len(devices)}")
    print("=" * 65)


def enrich_with_vendors(devices):
    """
    Adds vendor information to each device dict.
    Makes an API call per unique MAC OUI.
    """
    print("  Looking up vendors...")
    for device in devices:
        vendor = get_vendor(device["mac"])
        device["vendor"] = vendor
        print(f"  {device['ip']:<18} → {vendor}")
    return devices


def save_results(devices):
    """
    Saves the full scan results to a timestamped JSON file.
    """
    # Create results folder if it doesn't exist
    os.makedirs(RESULTS_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{RESULTS_FOLDER}/scan_{timestamp}.json"

    # Build the full report structure
    report = {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_devices": len(devices),
        "devices": devices
    }

    with open(filename, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n  Results saved → {filename}")
    return filename


# --- Quick test ---
if __name__ == "__main__":
    # Simulate what scanner.py found
    fake_devices = [
        {"ip": "192.168.1.102", "mac": "a0:59:50:7b:53:72"},
        {"ip": "192.168.1.1",   "mac": "00:1A:2B:3C:4D:5E"},
    ]

    print("Testing reporter with simulated devices...")
    enriched = enrich_with_vendors(fake_devices)
    display_table(enriched)
    save_results(enriched)