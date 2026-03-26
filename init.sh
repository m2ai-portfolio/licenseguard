#!/bin/bash
set -e

echo "Setting up LicenseGuard development environment..."

# Check Python version
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install click colorama pytest pydantic

# Install the package in development mode
pip install -e .

echo ""
echo "LicenseGuard development environment ready!"
echo "Run 'source venv/bin/activate' to activate the virtual environment."
echo "Then run 'licenseguard --help' to get started."
