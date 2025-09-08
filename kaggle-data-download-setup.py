import os
import sys
import subprocess
import stat
from pathlib import Path

# --- Configuration ---
# We'll tell the Kaggle API to look for the config file in our project root.
PROJECT_ROOT = Path(__file__).resolve().parent
KAGGLE_JSON_FILE = PROJECT_ROOT / "kaggle.json"

# Set the environment variable for the Kaggle library
os.environ['KAGGLE_CONFIG_DIR'] = str(PROJECT_ROOT)

DATA_DIR = PROJECT_ROOT / "data"
DATASET_NAME = "mlg-ulb/creditcardfraud"

def check_kaggle_credentials():
    """Checks for kaggle.json in the project root and verifies its permissions."""
    if not KAGGLE_JSON_FILE.exists():
        print("="*80)
        print("ERROR: Kaggle API credentials not found.")
        print(f"Please place your 'kaggle.json' file in the project root directory:")
        print(f"-> {PROJECT_ROOT}")
        print("\nInstructions:")
        print("1. Go to your Kaggle account settings: https://www.kaggle.com/account")
        print("2. Click on 'Create New API Token' to download 'kaggle.json'.")
        print(f"3. Move that file into your project folder.")
        print("="*80)
        sys.exit(1)

    # In Ubuntu/macOS, Kaggle API requires file permissions to be 600
    if sys.platform != 'win32':
        permissions = KAGGLE_JSON_FILE.stat().st_mode
        # Check if permissions are NOT read/write for owner only (600)
        if (permissions & (stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)):
            print("="*80)
            print("ERROR: 'kaggle.json' has incorrect permissions.")
            print("For security, the Kaggle API requires your credentials to be private.")
            print("\nPlease run the following command in your terminal to fix it:")
            print(f"  chmod 600 {KAGGLE_JSON_FILE}")
            print("="*80)
            sys.exit(1)

    print("Kaggle API credentials found and permissions are correct.")


def download_and_unzip_dataset():
    """Downloads and unzips the dataset from Kaggle."""
    DATA_DIR.mkdir(exist_ok=True)
    
    if (DATA_DIR / "creditcard.csv").exists():
        print(f"'creditcard.csv' already exists in the data directory. Skipping download.")
        return

    print(f"Downloading dataset '{DATASET_NAME}' from Kaggle...")
    
    command = [
        "kaggle", "datasets", "download",
        "-d", DATASET_NAME,
        "-p", str(DATA_DIR),
        "--unzip"
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("Dataset downloaded and unzipped successfully.")
    except subprocess.CalledProcessError as e:
        print("ERROR: Failed to download dataset from Kaggle.")
        print("Please ensure your kaggle.json is correctly configured and you have accepted the dataset's terms on the Kaggle website.")
        print(f"Kaggle API output:\n{e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("ERROR: 'kaggle' command not found.")
        print("Please ensure the Kaggle library is installed correctly (`pip install kaggle`).")
        sys.exit(1)


if __name__ == "__main__":
    print("--- Starting Project Setup ---")
    check_kaggle_credentials()
    download_and_unzip_dataset()
    print("--- Project Setup Complete ---")

