import os
import requests
from pathlib import Path
import pythoncom
import win32com.client

# ── Configuration ──────────────────────────────────────────────────────────────
REPO              = "SlingshotGoproAutomation/GoproAutomation"
EXE_NAME          = "Slingshot.exe"
DOWNLOAD_DIR      = Path(__file__).parent / "dist"
LAST_VERSION_FILE = DOWNLOAD_DIR / "last_version.txt"
GITHUB_API_LATEST = f"https://api.github.com/repos/{REPO}/releases/latest"
SHORTCUT_NAME     = "Slingshot"
# ────────────────────────────────────────────────────────────────────────────────

#Requests from Github Repository for latest Releases.
def get_latest_release_info():
    r = requests.get(GITHUB_API_LATEST) 
    r.raise_for_status()
    return r.json() 

#Returns current version tag number.
def get_local_version():
    if not LAST_VERSION_FILE.exists():
        return None
    return LAST_VERSION_FILE.read_text().strip()

#Updares LAST_VERSION_FILE with the latest tag.
def save_local_version(tag):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    LAST_VERSION_FILE.write_text(tag)

#Downloads the latest Slingshot.exe release to the correct diretory.
def download_asset(asset_url, target_path):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    with requests.get(asset_url, stream=True) as r:
        r.raise_for_status()
        with open(target_path, "wb") as f: 
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

#Creates a desktop shortcut for the latest Slingshot.exe file
def create_desktop_shortcut(target_path: Path, shortcut_name: str):
    desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
    shortcut_path = desktop / f"{shortcut_name}.lnk"

    # Initialize COM
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(str(shortcut_path))
    shortcut.Targetpath = str(target_path)
    shortcut.WorkingDirectory = str(target_path.parent)
    shortcut.IconLocation = str(target_path)  # use the exe as icon
    shortcut.Save()
  

def check_and_update():
    info       = get_latest_release_info() #Calls get_latest_release_info and gets return value in JSON format.
    latest_tag = info["tag_name"] #Info is a dictionary, "tag_name" is the key.
    local_tag  = get_local_version() #Calls get_local_version and gets return value

    if latest_tag == local_tag: #Compares tag number
        print(f"No new release. Already up to date. Version: {local_tag}")
        return

    # find the Slingshot.exe asset
    asset = next((a for a in info["assets"] if a["name"] == EXE_NAME), None)
    if not asset:
        print(f"ERROR: No asset named {EXE_NAME} found.")
        return

    target_path = DOWNLOAD_DIR / EXE_NAME #Creating target_path
    print(f"Downloading {EXE_NAME} to {target_path}...")
    download_asset(asset["browser_download_url"], target_path) #Calls download_asset function.
    save_local_version(latest_tag) #Calls save_local_version(latest_tag).
    print(f"Download complete. Version:{latest_tag}")

    # create/update the desktop shortcut
    create_desktop_shortcut(target_path, SHORTCUT_NAME) #Calls the create_desktop_shortcut function.
    print(f"Shortcut created: {shortcut_path}")
  
   
