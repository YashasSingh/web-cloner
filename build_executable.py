import subprocess
import sys
import os

# Change to the correct directory
os.chdir(r"c:\Users\ysingh\Downloads\new")

# Run PyInstaller
cmd = [
    r".venv\Scripts\python.exe",
    "-m", "PyInstaller",
    "--onefile",
    "--name", "WebsiteCloner",
    "website_cloner_main.py"
]

print("Building executable with PyInstaller...")
print("Command:", " ".join(cmd))

try:
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    print(f"Return code: {result.returncode}")
except Exception as e:
    print(f"Error: {e}")
