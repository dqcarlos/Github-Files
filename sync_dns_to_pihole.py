#!/usr/bin/env python3

import os
import paramiko
from datetime import datetime
from dotenv import load_dotenv

# === Load environment variables from .env (not committed to GitHub) ===
load_dotenv()

# === Configuration from environment ===
UNIFI_HOST = os.getenv("UNIFI_HOST")
UNIFI_USER = os.getenv("UNIFI_USER")
PIHOLE_HOST = os.getenv("PIHOLE_HOST")
PIHOLE_USER = os.getenv("PIHOLE_USER")
SSH_KEY_PATH = os.getenv("SSH_KEY_PATH")
LEASE_FILE = "/run/dns.conf.d/hosts.d/leases"
PIHOLE_CUSTOM_LIST = "/etc/pihole/custom.list"

def normalize_lines(text):
    return sorted(line.strip() for line in text.strip().splitlines() if line.strip())

# === Step 1: Get DHCP leases from UniFi Express ===
print("[+] Connecting to UniFi Express...")

unifi = paramiko.SSHClient()
unifi.set_missing_host_key_policy(paramiko.AutoAddPolicy())
unifi.connect(UNIFI_HOST, username=UNIFI_USER, key_filename=SSH_KEY_PATH)

stdin, stdout, stderr = unifi.exec_command(f"cat {LEASE_FILE}")
leases = stdout.read().decode().strip().splitlines()
unifi.close()

dns_entries = []
for line in leases:
    parts = line.split()
    if len(parts) == 2:
        ip, hostname = parts
        if not hostname.endswith(".lan"):
            hostname += ".lan"
        dns_entries.append(f"{ip} {hostname}")

print(f"[+] Parsed {len(dns_entries)} DNS entries.")

# === Step 2: SSH into Pi-hole ===
print("[+] Connecting to Pi-hole...")

pihole = paramiko.SSHClient()
pihole.set_missing_host_key_policy(paramiko.AutoAddPolicy())
pihole.connect(PIHOLE_HOST, username=PIHOLE_USER, key_filename=SSH_KEY_PATH)

# Read current custom.list
stdin, stdout, stderr = pihole.exec_command(f"cat {PIHOLE_CUSTOM_LIST} 2>/dev/null")
existing_data = stdout.read().decode()

existing_lines = normalize_lines(existing_data)
new_lines = normalize_lines("\n".join(dns_entries))

if existing_lines == new_lines:
    print("[✓] No changes detected — sync skipped.")
else:
    # Backup existing file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_cmd = f"sudo cp {PIHOLE_CUSTOM_LIST} {PIHOLE_CUSTOM_LIST}.bak.{timestamp}"
    pihole.exec_command(backup_cmd)
    print(f"[+] Backed up existing custom.list to custom.list.bak.{timestamp}")

    # Write new DNS entries
    entry_block = "\n".join(dns_entries) + "\n"
    write_cmd = f"echo '{entry_block}' | sudo tee {PIHOLE_CUSTOM_LIST} > /dev/null"
    pihole.exec_command(write_cmd)
    print("[+] Wrote new DNS entries to custom.list")

    # Restart Pi-hole DNS
    pihole.exec_command("pihole restartdns")
    print("[+] Restarted Pi-hole DNS")

pihole.close()
print("[✅] DNS sync complete.")