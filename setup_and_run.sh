#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.template .env
    echo "Please edit .env file and add your API key and default contract address before running the script."
    exit 1
fi

# Show usage
echo "Usage:"
echo "1. Run with default contract from .env:"
echo "   python snapshotActiveListings.py"
echo ""
echo "2. Run with specific contract:"
echo "   python snapshotActiveListings.py --contract 0xYOUR_CONTRACT_ADDRESS"
echo ""

# Ask if user wants to run with default contract
read -p "Do you want to run the script with the default contract? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    python snapshotActiveListings.py
fi

# Deactivate virtual environment
deactivate