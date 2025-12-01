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

Interactive menu to select tools

Custom wordlist support for Gobuster

### Installation

Clone the repository and make the script executable:

```
git clone https://github.com/Freeeedy/elucidator
cd elucidator
chmod +x tool.py
```

### Usage

Run the script:

```python3 tool.py```


You will be prompted for:

1. Target
```Target (IP/domain):```

2. Tools to run

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
0) Select all
```

Example:
```
Your choice: 1,4,7
```
3. Wordlist (only if Gobuster is selected)
Wordlist path:


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
