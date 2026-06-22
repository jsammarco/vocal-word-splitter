#!/usr/bin/env bash

set -e

VENV_DIR=".venv"

echo "Creating Python virtual environment..."

python3 -m venv "$VENV_DIR"

echo "Activating virtual environment..."

source "$VENV_DIR/bin/activate"

echo "Upgrading pip..."

python -m pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies..."

pip install -r requirements.txt

echo ""
echo "Setup complete."
echo ""
echo "To activate the virtual environment later, run:"
echo "source $VENV_DIR/bin/activate"
