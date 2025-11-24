import subprocess
import os
import platform
import argparse

os_name = platform.system()
parser = argparse.ArgumentParser(description='')

parser.add_argument('-t', type=str, required=True, help='what to scan')
parser.add_argument('-Nm', action='store_true', help='use nmap?')
parser.add_argument('-Na', action='store_true', help='use naabu?')
parser.add_argument('-Rs', action='store_true', help='use rustscan?')
parser.add_argument('-Gb', action='store_true', help='use gobuster?')
parser.add_argument('-Fb', action='store_true', help='use feroxbuster?')
parser.add_argument('-w', type=str, required=False, help='specify the wordlist path')

args = parser.parse_args()

if os_name == "Linux":
    if args.Nm == True:
        subprocess.Popen(f'nmap -sV {args.t} > nmap.log 2>&1', shell=True)
    if args.Na == True:
        subprocess.Popen(f'naabu -host {args.t} -timeout 500 -silent > naabu.log 2>&1', shell=True)
    if args.Rs == True:
        subprocess.Popen(f'rustscan -a {args.t} --no-banner --ulimit 5000 > rust.log 2>&1', shell=True)
    if args.Gb == True:
        subprocess.run(f'gobuster dir -u {args.t} -w {args.w} > gobuster.log 2>&1', shell=True)
    if args.Fb == True:
        subprocess.run(f'feroxbuster -u {args.t} -w {args.w} > feroxbuster.log 2>&1', shell=True)

elif os_name == "Windows":
    print('dont use that shit brother, windows sucks massive black dicks')