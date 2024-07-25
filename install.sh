#!/bin/bash

usage() {
    echo "[+] Usage: ./install.sh [--venv]"
    echo "[+] Options:"
    echo "[+]   --venv    Use a Python virtual environment (recommended)"
    exit 1
}

USE_VENV=false
if [[ "$1" == "--venv" ]]; then
    USE_VENV=true
fi

REPO_DIR="CIDRProbe"

if [ -d "$REPO_DIR" ]; then
    echo "[+] Repository already exists."
    echo "[+] Pulling the latest changes..."
    cd "$REPO_DIR" || { echo "[+] Error: Failed to enter the CIDRProbe directory."; exit 1; }
    git pull origin main
else
    echo "[+] Cloning the CIDRProbe repository..."
    git clone https://github.com/brian404/CIDRProbe.git
    cd "$REPO_DIR" || { echo "[+] Error: Failed to enter the CIDRProbe directory."; exit 1; }
fi

if ! command -v python3 &> /dev/null; then
    echo "[+] Error: Python3 is not installed. Please install Python3."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "[+] Error: pip is not installed. Please install pip."
    exit 1
fi

if [ "$USE_VENV" = true ]; then
    echo "[+] Setting up a virtual environment..."
    python3 -m venv .venv
    echo "[+] Activating the virtual environment..."
    source .venv/bin/activate
    echo "[+] Installing dependencies in the virtual environment..."
    python3 -m pip install -r requirements.txt
else
    echo "[+] Installing dependencies globally..."
    pip install -r requirements.txt
fi

echo "[+] Installation complete!"
echo "[+] To start using CIDR Probe, run the following command:"
echo "[+]   python cidr.py"
echo "[+] For advanced usage options, reefer to python cidr.py -h."

exit 0
