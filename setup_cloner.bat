@echo off
echo ========================================
echo Website Cloner Setup and Launch
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install requests beautifulsoup4 lxml

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup complete! Starting Website Cloner...
echo ========================================
echo.

python website_cloner_main.py

pause
