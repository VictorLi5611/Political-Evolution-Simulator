#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Print each command before executing it
set -x

# Create a Python virtual environment if it doesn't exist
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install required Python packages
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Install additional system dependencies if needed (uncomment and modify as necessary)
# brew install <package>
# sudo apt-get install <package>

echo "Setup complete."