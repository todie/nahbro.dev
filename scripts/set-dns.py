#!/usr/bin/env python3
"""
set-dns.py — Configure nahbro.dev DNS records on Namecheap for GitHub Pages.

Usage:
    python scripts/set-dns.py

Environment variables (required):
    NAMECHEAP_API_KEY      Your Namecheap API key
    NAMECHEAP_API_USER     Your Namecheap username (same as API username)

Optional:
    NAMECHEAP_CLIENT_IP    Your whitelisted IP (auto-detected via ipify if not set)
    NAMECHEAP_SANDBOX      Set to "1" to use sandbox API endpoint

Before running:
    1. Log in to Namecheap → Profile → Tools → API Access
    2. Enable API access
    3. Whitelist your current IP address
"""

import os
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET


DOMAIN_SLD = "nahbro"
DOMAIN_TLD = "dev"

A_RECORDS = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
]

CNAME_TARGET = "todie.github.io"

LIVE_API_URL = "https://api.namecheap.com/xml.response"
SANDBOX_API_URL = "https://api.sandbox.namecheap.com/xml.response"


def get_public_ip() -> str:
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as resp:
            return resp.read().decode().strip()
    except Exception as e:
        print(f"ERROR: Could not auto-detect public IP: {e}")
        print("Set NAMECHEAP_CLIENT_IP env var to your whitelisted IP and retry.")
        sys.exit(1)


def build_host_params() -> dict:
    params = {}
    index = 1
    for ip in A_RECORDS:
        params[f"HostName{index}"] = "@"
        params[f"RecordType{index}"] = "A"
        params[f"Address{index}"] = ip
        params[f"TTL{index}"] = "1800"
        index += 1
    params[f"HostName{index}"] = "www"
    params[f"RecordType{index}"] = "CNAME"
    params[f"Address{index}"] = CNAME_TARGET + "."
    params[f"TTL{index}"] = "1800"
    return params


def call_api(api_url: str, params: dict) -> ET.Element:
    url = f"{api_url}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            body = resp.read().decode()
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} from Namecheap API")
        print(e.read().decode())
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Network error: {e}")
        sys.exit(1)
    return ET.fromstring(body)


def check_response(root: ET.Element) -> bool:
    status = root.attrib.get("Status", "")
    if status == "ERROR":
        for err in root.iter("Error"):
            number = err.attrib.get("Number", "?")
            msg = err.text or "(no message)"
            print(f"  API Error [{number}]: {msg}")
            if number in ("1011150", "1011151"):
                print()
                print("  >> IP not whitelisted. Go to Namecheap → Profile → Tools → API Access")
                print("  >> and add your current public IP to the whitelist.")
        return False
    if status != "OK":
        print(f"  Unexpected status: {status}")
        print(ET.tostring(root, encoding="unicode"))
        return False
    for result in root.iter("DomainDNSSetHostsResult"):
        if result.attrib.get("IsSuccess", "false").lower() != "true":
            print("  setHosts returned IsSuccess=false")
            print(ET.tostring(result, encoding="unicode"))
            return False
    return True


def main():
    api_key = os.environ.get("NAMECHEAP_API_KEY", "").strip()
    api_user = os.environ.get("NAMECHEAP_API_USER", "").strip()
    client_ip = os.environ.get("NAMECHEAP_CLIENT_IP", "").strip()
    use_sandbox = os.environ.get("NAMECHEAP_SANDBOX", "").strip() == "1"

    if not api_key or not api_user:
        print("ERROR: NAMECHEAP_API_KEY and NAMECHEAP_API_USER must be set.")
        print()
        print("  export NAMECHEAP_API_KEY=your_key_here")
        print("  export NAMECHEAP_API_USER=your_username_here")
        sys.exit(1)

    if not client_ip:
        print("NAMECHEAP_CLIENT_IP not set — auto-detecting public IP...")
        client_ip = get_public_ip()
        print(f"  Detected IP: {client_ip}")
        print("  (Make sure this IP is whitelisted in Namecheap API Access settings)")

    api_url = SANDBOX_API_URL if use_sandbox else LIVE_API_URL
    env_label = "SANDBOX" if use_sandbox else "LIVE"

    print()
    print(f"Setting DNS records for {DOMAIN_SLD}.{DOMAIN_TLD} [{env_label}]")
    print()
    for ip in A_RECORDS:
        print(f"  A     @    → {ip}")
    print(f"  CNAME www  → {CNAME_TARGET}.")
    print()

    params = {
        "ApiUser": api_user,
        "ApiKey": api_key,
        "UserName": api_user,
        "ClientIp": client_ip,
        "Command": "namecheap.domains.dns.setHosts",
        "SLD": DOMAIN_SLD,
        "TLD": DOMAIN_TLD,
        **build_host_params(),
    }

    print("Calling Namecheap API...")
    root = call_api(api_url, params)

    if check_response(root):
        print("SUCCESS: DNS records updated.")
        print()
        print("Verify with: dig nahbro.dev A +short")
    else:
        print()
        print("FAILED: DNS records were NOT updated. See errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
