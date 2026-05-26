import json
from scapy.all import ARP, Ether, srp, conf

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

SUBNET = config["network"]["subnet"]
TIMEOUT = config["network"]["timeout_seconds"]
VERBOSE = config["network"]["verbose"]

# Tell Scapy not to print its own output
conf.verb = 0


def scan_network(subnet=None):
    """
    Sends ARP broadcast packets to every IP in the subnet.
    Any device that replies is alive — we record its IP and MAC.

    ARP works like this:
    Us:     "Hey everyone — who has IP 192.168.1.5? Tell 192.168.1.100"
    Device: "I have 192.168.1.5, my MAC is AA:BB:CC:DD:EE:FF"

    We do this for every IP in the subnet simultaneously.
    """

    if subnet is None:
        subnet = SUBNET

    print(f"\n  Scanning {subnet} ...")
    print(f"  Timeout per host: {TIMEOUT}s\n")

    # --- Build the ARP packet ---
    # Ether(dst="ff:ff:ff:ff:ff:ff") = broadcast frame (send to everyone)
    # ARP(pdst=subnet)               = ask "who has each IP in this subnet?"
    arp_request = ARP(pdst=subnet)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    # --- Send packet and collect replies ---
    # srp() = send and receive at Layer 2 (Ethernet level)
    # answered = list of (sent_packet, received_reply) pairs
    # unanswered = hosts that didn't reply (offline)
    answered, unanswered = srp(packet, timeout=TIMEOUT, verbose=VERBOSE)

    print(f"  Packets sent    : {len(answered) + len(unanswered)}")
    print(f"  Hosts responded : {len(answered)}")
    print(f"  Hosts silent    : {len(unanswered)}\n")

    # --- Extract IP and MAC from each reply ---
    devices = []
    for sent, received in answered:
        devices.append({
            "ip": received.psrc,    # psrc = protocol source (their IP)
            "mac": received.hwsrc   # hwsrc = hardware source (their MAC)
        })

    # Sort by IP address for clean output
    devices.sort(key=lambda x: list(map(int, x["ip"].split("."))))

    return devices


# --- Quick test ---
if __name__ == "__main__":
    print("=" * 50)
    print("  ARP Network Scanner — Test Run")
    print("=" * 50)

    devices = scan_network()

    if devices:
        print(f"  {'IP Address':<18} {'MAC Address'}")
        print(f"  {'-'*17} {'-'*17}")
        for d in devices:
            print(f"  {d['ip']:<18} {d['mac']}")
    else:
        print("  No devices found. Check your subnet in config.json")

    print(f"\n  Total: {len(devices)} devices found")