# Parallel Recon Toolkit

A fast, lightweight Python-based recon automation tool that runs multiple security scanning utilities in parallel, saving all output neatly into log files.
Made for authorized penetration testing, bug bounty recon, and CTF enumeration.
```
___________.__                .__    .___       __                
\_   _____/|  |  __ __   ____ |__| __| _/____ _/  |_  ___________ 
 |    __)_ |  | |  |  \_/ ___\|  |/ __ |\__  \\   __\/  _ \_  __ \
 |        \|  |_|  |  /\  \___|  / /_/ | / __ \|  | (  <_> )  | \/
/_______  /|____/____/  \___  >__\____ |(____  /__|  \____/|__|   
        \/                    \/        \/     \/                  
```
### Features

Run multiple recon tools simultaneously

Outputs results to logs/ directory

Supports major enumeration tools:
- nmap
- rustscan
- whatweb
- subfinder
- nikto
- smbmap
- nuclei
- gobuster
- waybackurls

- Deep port scan 
        - Combines Nmap + RustScan open port results
        - Automatically runs port-specific enumeration modules
        - Outputs saved into logs/deep/ and logs/ports/

### Configurable Commands (config.json)

All tool commands are now stored in a central config file:
`config.json`
```
{
    "tools": {
        "nmap": "nmap -sV {target}",
        "rustscan": "rustscan -a {target}",
        "whatweb": "whatweb {target}",
        "subfinder": "subfinder -d {target} -o subs.txt",
        "nikto": "nikto -host {target}",
        "smbmap": "smbmap -H {target}",
        "nuclei": "nuclei -u {target}",
        "gobuster": "gobuster dir -u http://{target} -w {wordlist}",
        "waybackurls": "echo {target} | waybackurls"
    }
}

```
You can freely modify these to change tool arguments, for example:
- switch `nmap -sV` → `nmap -A`
- use custom nuclei templates
- change rustscan ports
- add your own tools

No code changes required.

To use a custom config:
```
python3 elucidator.py --config myconfig.json
```


### Installation

Clone the repository and make the script executable:

```
git clone <your-repo>
cd <your-repo>
chmod +x tool.py
```

Install necessary tools:
```
./install.sh
```

### Usage

Run the script:
```
python3 tool.py
```

You will be prompted for:

##### 1. Target
```
Target (IP/domain):
```
##### 2. Tools to run

```
Select one or more tools:

1) Nmap
2) RustScan
3) WhatWeb
4) Subfinder
5) Nikto
6) SMBMap
7) Nuclei
8) Gobuster
9) WayBackURLs
10) Deep port scan
0) Select all
```

Example:
```
Your choice: 1,4,7
```
##### 3. Wordlist (only if Gobuster is selected)
```
Wordlist path:
```
If empty, it defaults to:
```
wordlists/directory-list-2.3-medium.txt
```

### Output

All logs are saved inside the folder:
```
logs/
│── nmap.log
│── rustscan.log
│── whatweb.log
│── ...
```

Each tool runs in the background and the script waits for all jobs to finish.

### Deep Port Scan

The new Deep Port Scan mode performs a multi-stage, automated port-specific enumeration:

##### Step 1 — Dual open-port detection

Runs both:
- nmap
- rustscan

Open ports are extracted and merged into:
```
logs/deep/open_ports.txt
```
##### Step 2 — Port-specific modules

Each detected port is checked against a module list:
```
PORT_MODULES = {
 21: ftp_enum
 22: ssh-audit
 23: telnet-encryption script
 25: smtp-user-enum
 53: dnsenum
 ...
 27017: mongo stats
}
```
If a module exists for that port, it is automatically executed:
```
logs/ports/<port>.log
```
Example output:
```
[+] Port 445 matched → running: smbmap -H <target>
[✓] Output saved to logs/ports/445.log
[-] No module for port 5353
```

This allows ultra-fast recon → enumeration chaining with no manual steps.

**Note:**

Elu 0.1 was fully coded by me. Starting from Elu 1.0, I expanded the project with additional features and improvements. The majority of the code is still written by me, with supplemental assistance and ideas provided through Vibe Coding.
