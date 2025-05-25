from pathlib import Path

# Directory for storing alert logs
ALERTS_DIR = Path("alerts")

# Ensure the alerts directory exists
ALERTS_DIR.mkdir(exist_ok=True) 