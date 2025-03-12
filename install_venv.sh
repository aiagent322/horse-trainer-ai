#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$SCRIPT_DIR" || exit

# Function to prompt the user for yes/no response
prompt_yes_no() {
    while true; do
        read -p "$1 (y/n): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes (y) or no (n).";;
        esac
    done
}

# Check if venv exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Do you want to recreate it?"
    if prompt_yes_no "Recreate virtual environment?"; then
        rm -rf venv
    else
        echo "Using existing virtual environment."
        exit 0
    fi
fi

# Ensure Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in PATH."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
venv/bin/pip install --upgrade pip

echo "Virtual environment setup complete!"

