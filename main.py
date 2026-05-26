import json
from datetime import datetime
from scanner import scan_network
from reporter import enrich_with_vendors, display_table, save_results

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

SUBNET = config["network"]["subnet"]


def run_scanner():
    print("=" * 65)
    print("  ARP Network Scanner & Device Mapper")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    # Step 1 — Scan the network
    devices = scan_network(SUBNET)

    if not devices:
        print("  No devices found. Check subnet in config.json")
        return

    # Step 2 — Enrich with vendor info
    print("-" * 65)
    enriched = enrich_with_vendors(devices)

    # Step 3 — Display results table
    display_table(enriched)

    # Step 4 — Flag anything suspicious
    print("\n  Security Analysis:")
    print("-" * 65)
    flag_count = 0
    for device in enriched:
        if device["vendor"] == "Unknown":
            print(f"  ⚠ UNKNOWN VENDOR — {device['ip']} ({device['mac']}) — investigate")
            flag_count += 1

    if flag_count == 0:
        print("  ✓ All devices have known vendors — nothing suspicious")

    # Step 5 — Save results to JSON
    save_results(enriched)

    print(f"\n  Scan complete — {len(enriched)} devices mapped")
    print("=" * 65)


if __name__ == "__main__":
    run_scanner()