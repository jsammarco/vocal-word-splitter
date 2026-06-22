@echo off
setlocal

set "VENV_DIR=.venv"

if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Virtual environment not found at %VENV_DIR%.
    echo Run setup first.
    pause
    exit /b 1
)

call "%VENV_DIR%\Scripts\activate.bat"

echo.
echo Virtual environment activated.
echo Type commands below. Use "deactivate" to exit the venv.
echo.

cmd /k