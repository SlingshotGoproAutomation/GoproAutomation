import schedule
import time
import requests
import os

# --- Config ---
REPO = "SlingshotGoproAutomation/GoproAutomation"
LAST_VERSION_FILE = "last_version.txt"
EXE_NAME = "main.exe"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"

# --- Functions ---
def get_latest_release_info():
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    return response.json()

def get_local_version():
    if not os.path.exists(LAST_VERSION_FILE):
        return None
    with open(LAST_VERSION_FILE, "r") as f:
        return f.read().strip()

def save_local_version(tag):
    with open(LAST_VERSION_FILE, "w") as f:
        f.write(tag)

def download_exe(download_url):
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(EXE_NAME, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded new version: {EXE_NAME}")

def check_for_new_release():
    latest_info = get_latest_release_info()
    latest_tag = latest_info["tag_name"]
    local_tag = get_local_version()

    if latest_tag != local_tag:
        print(f"New release detected: {latest_tag}")
        asset = next((a for a in latest_info["assets"] if a["name"] == EXE_NAME), None)
        if asset:
            download_exe(asset["browser_download_url"])
            save_local_version(latest_tag)
        else:
            print(f"ERROR: No asset named {EXE_NAME} found in latest release.")
    else:
        print("No new release. Already up to date.")

# --- Scheduler setup ---
schedule.every().day.at("10:00").do(check_for_new_release)

print("Updater is running. Waiting for the next scheduled time...")

while True:
    schedule.run_pending()
    time.sleep(60)
