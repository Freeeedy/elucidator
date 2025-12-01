#!/bin/bash

echo "[+] Updating system..."
sudo apt update -y
sudo apt install -y git curl wget python3 python3-pip cargo build-essential

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

echo "[✓] All tools installed successfully!"
