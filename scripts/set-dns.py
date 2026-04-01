#!/usr/bin/env python3
"""
set-dns.py — nahbro.dev DNS records via Namecheap API.

Usage:
    python scripts/set-dns.py

Environment variables (required):
    NAMECHEAP_API_KEY      Your Namecheap API key
    NAMECHEAP_API_USER     Your Namecheap username

Optional:
    NAMECHEAP_CLIENT_IP    Your whitelisted IP (auto-detected if not set)
    NAMECHEAP_SANDBOX      Set to "1" for sandbox endpoint

Before running:
    Namecheap → Profile → Tools → API Access → enable + whitelist IP
"""

import os
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET


DOMAIN_SLD = "nahbro"
DOMAIN_TLD = "dev"

RECORDS = [
    # GitHub Pages A records
    ("@",   "A",     "185.199.108.153"),
    ("@",   "A",     "185.199.109.153"),
    ("@",   "A",     "185.199.110.153"),
    ("@",   "A",     "185.199.111.153"),
    # www CNAME
    ("www", "CNAME", "todie.github.io."),
    # GitHub Pages domain verification
    ("_github-pages-challenge-todie", "TXT", "f0829e2aa39f3bada9851d66928ed5"),
]

LIVE_API_URL    = "https://api.namecheap.com/xml.response"
SANDBOX_API_URL = "https://api.sandbox.namecheap.com/xml.response"


def get_public_ip() -> str:
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as r:
            return r.read().decode().strip()
    except Exception as e:
        print(f"ERROR: Could not auto-detect public IP: {e}")
        print("Set NAMECHEAP_CLIENT_IP and retry.")
        sys.exit(1)


def build_host_params() -> dict:
    params = {}
    for i, (host, rtype, addr) in enumerate(RECORDS, 1):
        params[f"HostName{i}"]   = host
        params[f"RecordType{i}"] = rtype
        params[f"Address{i}"]    = addr
        params[f"TTL{i}"]        = "1800"
    return params


def call_api(api_url: str, params: dict) -> ET.Element:
    url = f"{api_url}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return ET.fromstring(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code}")
        print(e.read().decode())
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def check_response(root: ET.Element) -> bool:
    status = root.attrib.get("Status", "")
    if status == "ERROR":
        for err in root.iter("Error"):
            num = err.attrib.get("Number", "?")
            print(f"  [{num}]: {err.text}")
            if num in ("1011150", "1011151"):
                print("  >> whitelist your IP at Namecheap → Profile → Tools → API Access")
        return False
    if status != "OK":
        print(f"  unexpected status: {status}")
        return False
    for r in root.iter("DomainDNSSetHostsResult"):
        if r.attrib.get("IsSuccess", "").lower() != "true":
            print("  IsSuccess=false")
            return False
    return True


def main():
    api_key   = os.environ.get("NAMECHEAP_API_KEY",  "").strip()
    api_user  = os.environ.get("NAMECHEAP_API_USER", "").strip()
    client_ip = os.environ.get("NAMECHEAP_CLIENT_IP","").strip()
    sandbox   = os.environ.get("NAMECHEAP_SANDBOX",  "").strip() == "1"

    if not api_key or not api_user:
        print("NAMECHEAP_API_KEY and NAMECHEAP_API_USER required")
        sys.exit(1)

    if not client_ip:
        client_ip = get_public_ip()
        print(f"IP: {client_ip}")

    api_url = SANDBOX_API_URL if sandbox else LIVE_API_URL
    print(f"\nSetting DNS for {DOMAIN_SLD}.{DOMAIN_TLD} [{'SANDBOX' if sandbox else 'LIVE'}]\n")
    for host, rtype, addr in RECORDS:
        print(f"  {rtype:<5} {host:<35} → {addr}")
    print()

    params = {
        "ApiUser": api_user, "ApiKey": api_key,
        "UserName": api_user, "ClientIp": client_ip,
        "Command": "namecheap.domains.dns.setHosts",
        "SLD": DOMAIN_SLD, "TLD": DOMAIN_TLD,
        **build_host_params(),
    }

    root = call_api(api_url, params)
    if check_response(root):
        print("done.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
