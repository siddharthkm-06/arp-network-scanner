import urllib.request
import json
import time

# Simple in-memory cache so we don't look up the same MAC twice
_cache = {}

def get_vendor(mac):
    """
    Looks up the hardware vendor for a given MAC address.
    Uses the free macvendors.com API — no key needed.
    
    MAC OUI = first 3 bytes (6 characters)
    Example: a0:59:50:7b:53:72 → OUI is a0:59:50 → lookup who makes it
    """

    # Extract just the OUI (first 3 octets)
    oui = mac[:8].upper()

    # Return from cache if we already looked this up
    if oui in _cache:
        return _cache[oui]

    try:
        # Build the API URL
        url = f"https://api.macvendors.com/{oui}"

        # Make the HTTP request with a 3 second timeout
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "arp-scanner/1.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            vendor = response.read().decode("utf-8").strip()

        # Cache the result
        _cache[oui] = vendor

        # Small delay to be polite to the free API (rate limit)
        time.sleep(0.5)

        return vendor

    except Exception:
        # If lookup fails for any reason, just return Unknown
        _cache[oui] = "Unknown"
        return "Unknown"


# --- Quick test ---
if __name__ == "__main__":
    test_macs = [
        "a0:59:50:7b:53:72",   # from your scan
        "00:1A:2B:3C:4D:5E",   # random test
    ]

    print("MAC Vendor Lookup Test")
    print("-" * 40)
    for mac in test_macs:
        vendor = get_vendor(mac)
        print(f"  {mac}  →  {vendor}")