# ARP Network Scanner & Device Mapper

A Python-based network reconnaissance tool that crafts raw ARP packets
at Layer 2 (Ethernet level) to discover all live devices on a subnet,
resolve hardware vendors via OUI lookup, flag unknown devices, and export
the full network topology as structured JSON.

Built to simulate real-world network discovery and asset inventory workflows.

---

## What Problem Does This Solve?

Network engineers need to know exactly what devices are on their network at
any given time. Unknown or unauthorized devices are a security and operational
risk. This tool automates subnet-wide discovery in seconds — identifying every
live host, its MAC address, its hardware vendor, and flagging anything suspicious.

---

## Features

- Crafts raw ARP broadcast packets using Scapy at Layer 2
- Discovers all live hosts across a /24 subnet in under 5 seconds
- Resolves hardware vendor from MAC OUI via macvendors.com API
- Flags devices with unknown or randomized MACs as suspicious
- Exports full topology as timestamped JSON for documentation
- All settings configurable via config.json

---

## Project Structure

arp_scanner/
├── config.json      # Subnet target and scan settings
├── scanner.py       # Raw ARP packet engine — core discovery logic
├── vendor.py        # MAC OUI vendor lookup with caching
├── reporter.py      # Table display + JSON export
├── main.py          # Orchestrates full scan pipeline
└── results/
└── scan_YYYY-MM-DD_HH-MM-SS.json

---

## Sample Output

<img width="682" height="568" alt="Screenshot 2026-05-26 210003" src="https://github.com/user-attachments/assets/1ab458ef-3d2b-48fd-96c1-3147177c441f" />

<img width="721" height="199" alt="Screenshot 2026-05-26 210702" src="https://github.com/user-attachments/assets/d335ba2a-884d-4e52-9188-11f4ad06cf81" />

---

## How to Run

**Requirements:** Python 3.8+, Scapy, Npcap (Windows)

```bash
# Install Npcap first (Windows only)
# Download from npcap.com and install with default options

# Install Scapy
pip install scapy

# Clone the repo
git clone https://github.com/siddharthkm-06/arp-network-scanner.git
cd arp-network-scanner

# Run as Administrator (required for raw packet crafting)
python main.py
```

---

## Configuration

Edit config.json to target a different subnet:

```json
{
  "network": {
    "subnet": "192.168.1.0/24",
    "timeout_seconds": 2,
    "verbose": false
  }
}
```

---

## Sample JSON Output

```json
{
  "scan_time": "2026-05-26 20:58:15",
  "total_devices": 4,
  "devices": [
    {
      "ip": "192.168.1.1",
      "mac": "aa:bb:cc:dd:ee:ff",
      "vendor": "TP-Link Systems Inc"
    },
    {
      "ip": "192.168.1.100",
      "mac": "bb:cc:dd:ee:ff:00",
      "vendor": "HP Inc."
    },
    {
      "ip": "192.168.1.102",
      "mac": "cc:dd:ee:ff:00:11",
      "vendor": "Unknown"
    },
    {
      "ip": "192.168.1.104",
      "mac": "7a:00:aa:bb:cc:dc",
      "vendor": "Unknown"
    }
  ]
}
```

---

## Key Technical Concepts Demonstrated

- **ARP protocol** — Layer 2 device discovery below IP level
- **Raw packet crafting** — Scapy Ether/ARP packet construction
- **MAC OUI lookup** — hardware vendor identification
- **Broadcast networking** — ff:ff:ff:ff:ff:ff frame addressing
- **Randomized MAC detection** — identifying privacy-masked devices
- **JSON topology export** — structured data for further processing

---

## Real-World Relevance

- Device discovery → matches network asset inventory workflows
- Unknown vendor flagging → matches unauthorized device detection
- JSON export → matches integration with CMDB/IPAM systems
- Layer 2 operation → demonstrates protocol knowledge below TCP/IP

