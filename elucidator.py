import subprocess
import os

ASCII = r"""
___________.__                .__    .___       __                
\_   _____/|  |  __ __   ____ |__| __| _/____ _/  |_  ___________ 
 |    __)_ |  | |  |  \_/ ___\|  |/ __ |\__  \\   __\/  _ \_  __ \
 |        \|  |_|  |  /\  \___|  / /_/ | / __ \|  | (  <_> )  | \/
/_______  /|____/____/  \___  >__\____ |(____  /__|  \____/|__|   
        \/                    \/        \/     \/                  
"""

# Tools to select from
TOOLS = {
    "nmap":      "nmap -sV {target}",
    "rustscan":  "rustscan -a {target} --ulimit 5000 --no-banner",
    "whatweb":   "whatweb {target} --color=never",
    "subfinder": "subfinder -d {target} -silent",
    "nikto":     "nikto -h {target}",
    "smbmap":    "smbmap -H {target}",
    "nuclei":    "nuclei -u {target} -silent",
    "gobuster":  "gobuster dir -u {target} -w {wordlist} -q",
    "waybackurls": "waybackurls {target}"}

# Port-specific tools for deep port scan
PORT_MODULES = {
    21:  "ftp_enum {target}",
    22:  "ssh-audit {target}",
    23:  "nmap --script telnet-encryption {target}",
    25:  "smtp-user-enum -M VRFY -U wordlist.txt -t {target}",
    53:  "dnsenum {target}",
    80:  "whatweb {target}",
    110: "nmap --script pop3-capabilities {target}",
    111: "showmount -e {target}",
    139: "smbmap -H {target}",
    143: "nmap --script imap-capabilities {target}",
    389: "windapsearch -d domain.local -u '' --dc-ip {target}",
    443: "whatweb {target}",
    445: "smbmap -H {target}",
    587: "smtp-user-enum -M VRFY -U wordlist.txt -t {target}",
    631: "nmap --script ipp-enum {target}",
    873: "rsync --list-only rsync://{target}/",
    1025: "nmap --script rpcinfo {target}",
    1433: "impacket-mssqlclient sa:''@{target}",
    1521: "tnscmd10g version -h {target}",
    2049: "showmount -e {target}",
    3128: "nmap --script http-open-proxy {target}",
    3306: "nmap --script mysql-enum {target}",
    3389: "rdp-sec-check {target}",
    5432: "nmap --script pgsql-brute {target}",
    5900: "nmap --script vnc-info {target}",
    5985: "evil-winrm -i {target}",
    6379: "redis-cli -h {target} INFO",
    8000: "whatweb {target}",
    8080: "whatweb {target}",
    8443: "whatweb {target}",
    9050: "nmap --script socks-open-proxy {target}",
    11211: "memcached-tool {target} stats",
    27017: "mongo --host {target} --eval 'db.stats()'",}

# Ask for the target
def ask_target():
    return input("Target (IP/domain): ").strip()

# Ask what tool to use
def ask_tools():
    print("\nSelect tools (comma-separated):")
    print(" 1) Nmap")
    print(" 2) RustScan")
    print(" 3) WhatWeb")
    print(" 4) Subfinder")
    print(" 5) Nikto")
    print(" 6) SMBMap")
    print(" 7) Nuclei")
    print(" 8) Gobuster")
    print(" 9) WayBackURLs")
    print(" 10) Deep port scan")
    print(" 0) Select All\n")

    # Split the choices by ","
    choices = input("Your choice: ").replace(" ", "").split(",")
    selected = []

    # Append the selected tools to selected
    for c in choices:
        if c == "1": selected.append("nmap")
        elif c == "2": selected.append("rustscan")
        elif c == "3": selected.append("whatweb")
        elif c == "4": selected.append("subfinder")
        elif c == "5": selected.append("nikto")
        elif c == "6": selected.append("smbmap")
        elif c == "7": selected.append("nuclei")
        elif c == "8": selected.append("gobuster")
        elif c == "9": selected.append("waybackurls")
        elif c == "10": selected.append("deep_port_scan")
        elif c == "0": selected.extend(["nmap", "rustscan", "whatweb", "subfinder", "nikto", "smbmap", "nuclei", "gobuster", "waybackurls"])

    return selected

# If gobuster is in selected ask for the wordlist path
def ask_wordlist(selected):
    if "gobuster" in selected:
        return input("Wordlist path: ").strip()
    return None


def run_tools_parallel(target, selected, wordlist):
    os.makedirs("logs", exist_ok=True)
    processes = []

    # Default wordlist
    if wordlist == "":
        wordlist = "wordlists/directory-list.txt"

    # Run normal tools in parallel (skip deep scan)
    for tool in selected:
        if tool == "deep_port_scan":
            continue

        cmd = TOOLS[tool].format(target=target, wordlist=wordlist)
        logfile = f"logs/{tool}.log"

        print(f"[+] Starting {tool} in background: {cmd}")

        f = open(logfile, "w")
        p = subprocess.Popen(cmd, shell=True, stdout=f, stderr=f)
        processes.append((tool, p, f))

    print("\n[+] All selected tools are running in parallel...\n")

    # Wait for all normal tools to finish
    for tool, proc, f in processes:
        proc.wait()
        f.close()
        print(f"[✓] {tool} finished → logs/{tool}.log")

    # Now run deep scan (AFTER nmap + rustscan completed)
    if "deep_port_scan" in selected:
        deep_scan(target)

def deep_scan(target):
    print("\n[+] Starting deep port scan AFTER base scans completed...")

    os.makedirs("logs/deep", exist_ok=True)
    os.makedirs("logs/ports", exist_ok=True)

    nmap_dp = (
        f'nmap --open -oX - {target} | '
        'xmlstarlet sel -t -m "//port[state/@state=\'open\']" '
        '-v "@portid" -n > logs/deep/nmap_ports.txt'
    )
    
    p1 = subprocess.Popen(nmap_dp, shell=True)

    rustscan_dp = (
        f"rustscan -a {target} | grep 'Open' | awk '{{print $2}}' "
        "| cut -d/ -f1 > logs/deep/rustscan_ports.txt"
    )

    p2 = subprocess.Popen(rustscan_dp, shell=True)

    # Wait for both scans to finish
    p1.wait()
    p2.wait()

    merged_path = "logs/deep/open_ports.txt"
    ports = set()

    # Read Nmap ports
    if os.path.exists("logs/deep/nmap_ports.txt"):
        with open("logs/deep/nmap_ports.txt") as f:
            for line in f:
                if line.strip().isdigit():
                    ports.add(int(line.strip()))

    # Read RustScan ports
    if os.path.exists("logs/deep/rustscan_ports.txt"):
        with open("logs/deep/rustscan_ports.txt") as f:
            for line in f:
                if line.strip().isdigit():
                    ports.add(int(line.strip()))

    # Save merged ports
    with open(merged_path, "w") as f:
        for p in sorted(ports):
            f.write(f"{p}\n")

    print(f"[+] Open ports found: {sorted(ports)}")
    print("[+] Running associated port enumeration modules...")

    # Run port-specific modules
    for port in sorted(ports):
        if port in PORT_MODULES:
            module_cmd = PORT_MODULES[port].format(target=target)
            out_file = f"logs/ports/{port}.log"

            print(f"[+] Port {port} matched → running: {module_cmd}")

            with open(out_file, "w") as f:
                subprocess.Popen(module_cmd, shell=True, stdout=f, stderr=f).wait()

            print(f"[✓] Output saved to {out_file}")
        else:
            print(f"[-] No module for port {port}")

    return sorted(ports)

def main():
    print(ASCII)
    print("Use only on systems you are authorized to test.\n")

    target = ask_target()
    selected = ask_tools()
    wordlist = ask_wordlist(selected)

    run_tools_parallel(target, selected, wordlist)

    print("\nAll tasks complete. Check the logs/ folder!")


if __name__ == "__main__":
    main()
