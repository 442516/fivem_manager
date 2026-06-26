@echo off
chcp 65001 >nul
python fivem_manager.py
if errorlevel 1 (
    echo.
    echo [ERROR] Python not found. Please install Python 3 from https://python.org
    echo        Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
)
