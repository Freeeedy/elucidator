#!/bin/bash

echo "[+] Updating system..."
sudo apt update -y
sudo apt install -y git curl wget python3 python3-pip cargo build-essential

echo "[+] Installing Argparse"
sudo pip install argparse

echo "[+] Installing Nmap..."
sudo apt install -y nmap

echo "[+] Installing RustScan..."
cargo install rustscan
sudo ln -s ~/.cargo/bin/rustscan /usr/local/bin/rustscan 2>/dev/null

echo "[+] Installing WhatWeb..."
sudo apt install -y whatweb

echo "[+] Installing Go..."
sudo apt install -y golang

echo "[+] Setting GOPATH..."
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

echo "[+] Installing Subfinder..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
sudo mv ~/go/bin/subfinder /usr/local/bin/ 2>/dev/null

echo "[+] Installing Nuclei..."
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
sudo mv ~/go/bin/nuclei /usr/local/bin/ 2>/dev/null

echo "[+] Installing WaybackURLs..."
go install github.com/tomnomnom/waybackurls@latest
sudo mv ~/go/bin/waybackurls /usr/local/bin/ 2>/dev/null

echo "[+] Installing Gobuster..."
sudo apt install -y gobuster

echo "[+] Installing Nikto..."
sudo apt install -y nikto

echo "[+] Installing SMBMap..."
sudo apt install -y smbmap

echo "[+] Installing ftp enum tools..."
sudo apt install -y ftp

echo "[+] Installing ssh-audit..."
sudo pip3 install ssh-audit

echo "[+] Installing smtp-user-enum..."
sudo apt install -y smtp-user-enum

echo "[+] Installing dnsenum..."
sudo apt install -y dnsenum

echo "[+] Installing showmount (NFS utils)..."
sudo apt install -y nfs-common

echo "[+] Installing windapsearch..."
sudo git clone https://github.com/ropnop/windapsearch /opt/windapsearch
sudo ln -s /opt/windapsearch/windapsearch.py /usr/local/bin/windapsearch 2>/dev/null

echo "[+] Installing rsync..."
sudo apt install -y rsync

echo "[+] Installing Impacket..."
sudo apt install -y python3-impacket

echo "[+] Installing RDP Security Check..."
sudo git clone https://github.com/robertdavidgraham/rdp-sec-check /opt/rdp-sec-check
sudo make -C /opt/rdp-sec-check
sudo ln -s /opt/rdp-sec-check/rdp-sec-check /usr/local/bin/rdp-sec-check 2>/dev/null

echo "[+] Installing Evil-WinRM..."
sudo gem install evil-winrm

echo "[+] Installing Redis CLI..."
sudo apt install -y redis-tools

echo "[+] Installing memcached-tool..."
sudo apt install -y memcached

echo "[+] Installing MongoDB client..."
sudo apt install -y mongodb-clients

echo "[✓] All tools installed successfully!"
