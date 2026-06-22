$ErrorActionPreference = "Stop"

$VENV_DIR = ".venv"

Write-Host "Creating Python virtual environment..."

python -m venv $VENV_DIR

Write-Host "Activating virtual environment..."

& "$VENV_DIR\Scripts\Activate.ps1"

Write-Host "Upgrading pip..."

python -m pip install --upgrade pip setuptools wheel

Write-Host "Installing Python dependencies..."

pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete."
Write-Host ""
Write-Host "To activate the virtual environment later, run:"
Write-Host "$VENV_DIR\Scripts\Activate.ps1"