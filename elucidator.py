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


def ask_target():
    return input("Target (IP/domain): ").strip()


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
    print(" 0) select all\n")

    choices = input("Your choice: ").replace(" ", "").split(",")
    selected = []

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
        elif c == "0": selected.extend(["nmap", "rustscan", "whatweb", "subfinder", "nikto", "smbmap", "nuclei", "gobuster", "waybackurls"])

    return selected


def ask_wordlist(selected):
    if "gobuster" in selected:
        return input("Wordlist path: ").strip()
    return None


def run_tools_parallel(target, selected, wordlist):
    os.makedirs("logs", exist_ok=True)

    processes = []

    # Default wordlist
    if wordlist == "":
        wordlist = "wordlists/directory-list-2.3-medium.txt"

    for tool in selected:
        cmd = TOOLS[tool].format(target=target, wordlist=wordlist)
        logfile = f"logs/{tool}.log"

        print(f"[+] Starting {tool} in background: {cmd}")

        f = open(logfile, "w")
        p = subprocess.Popen(cmd, shell=True, stdout=f, stderr=f)
        processes.append((tool, p, f))

    print("\n[+] All selected tools are running in parallel...\n")

    for tool, proc, f in processes:
        proc.wait()
        f.close()
        print(f"[✓] {tool} finished → logs/{tool}.log")


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
