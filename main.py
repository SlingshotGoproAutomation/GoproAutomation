import requests
from bs4 import BeautifulSoup
import os
import io
import qrcode
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from datetime import datetime
import webbrowser
import urllib.parse
import platform
import subprocess
import json
import sys
import schedule
import time
import CheckLatestUpdate
import traceback
from pathlib import Path

# --- Constants ---
DIST_FOLDER = CheckLatestUpdate.get_base_dir() / "dist"
print(f"My dist folder is at: {DIST_FOLDER}")

# --- Helper to get resource paths ---
def resource_path(filename):
    if getattr(sys, 'frozen', False):
        print("Running from a PyInstaller bundle.")
        return os.path.join(sys._MEIPASS, filename)
    else:
        print("Running from normal Python environment.")
        return os.path.join(os.path.abspath("."), filename)

# --- Load configuration ---
config_path = resource_path("config.json")
print("Resolved config.json path:", config_path)

# Check if file exists before loading
if not os.path.exists(config_path):
    raise FileNotFoundError(f"config.json not found at: {config_path}")

with open(config_path, "r") as config_file:
    config = json.load(config_file)
print("Config loaded successfully.")

GOPRO_BASE_URL = "http://10.5.5.9/videos/DCIM/100GOPRO/"
GOOGLE_DRIVE_FOLDER_ID = config["GOOGLE_DRIVE_FOLDER_ID"]
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SERVICE_ACCOUNT_FILE = config["SERVICE_ACCOUNT_FILE"]

creds = Credentials.from_service_account_file(resource_path(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# --- Set base and date folder ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(sys.executable), os.pardir))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

today_str = datetime.now().strftime("%d-%m-%y")
day_folder = os.path.join(BASE_DIR, today_str)
os.makedirs(day_folder, exist_ok=True)

# --- GoPro Functions ---
def get_latest_video_file():
    try:
        response = requests.get(GOPRO_BASE_URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            video_files = [link.get('href') for link in soup.find_all('a')
                           if link.get('href') and link.get('href').endswith('.MP4')]
            if video_files:
                return sorted(video_files, reverse=True)[0]
            else:
                print("No video files found in the directory.")
        else:
            print("Failed to connect to the GoPro.")
    except Exception as e:
        print(f"Error accessing the GoPro directory: {e}")
    return None

def download_video(latest_video):
    local_video_file = os.path.basename(latest_video)
    local_path = os.path.join(day_folder, local_video_file)

    print(f"Downloading the latest video: {latest_video}")
    video_url = f"{GOPRO_BASE_URL}{latest_video}" if not latest_video.startswith("/videos/") else f"http://10.5.5.9{latest_video}"
    print(f"Attempting to download from URL: {video_url}")

    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(local_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"✅ Video downloaded successfully: {local_path}")
        return local_path
    else:
        print(f"Failed to download the video. HTTP Status Code: {response.status_code}")
        return None

def upload_video_to_drive(local_video_file):
    try:
        file_metadata = {'name': os.path.basename(local_video_file), 'parents': [GOOGLE_DRIVE_FOLDER_ID]}
        media = MediaFileUpload(local_video_file, mimetype='video/mp4', resumable=True)
        request = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink')

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploading... {int(status.progress() * 100)}%")

        print(f"✅ Video uploaded to Google Drive: {response['webViewLink']}")
        return response['webViewLink']
    except Exception as e:
        print(f"❌ Error uploading video to Google Drive: {e}")
        return None

def generate_qr_code(video_link):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(video_link)
    qr.make(fit=True)

    qr_image_path = os.path.join(day_folder, "video_qr_code.png")
    img = qr.make_image(fill='black', back_color='white')
    img.save(qr_image_path)

    print(f"✅ QR Code saved at: {qr_image_path}")

    try:
        if platform.system() == "Windows":
            os.system(f'start "" "{qr_image_path}"')
        elif platform.system() == "Darwin":
            subprocess.run(["open", qr_image_path], check=True)
        else:
            subprocess.run(["xdg-open", qr_image_path], check=True)
        print("✅ QR Code opened successfully.")
    except Exception as e:
        print(f"❌ Error opening QR Code: {e}")

    return qr_image_path


def job_check_update():
    try:
        CheckLatestUpdate.check_and_update()
        new_exe = DIST_FOLDER / "Slingshot_new.exe"

        if new_exe.exists():
            print("New version downloaded. Launching updater...")

            # 1. Handle both EXE and script mode
            if getattr(sys, 'frozen', False):
                exe_dir = Path(sys.executable).resolve().parent
            else:
                # Use script directory when running from source
                exe_dir = Path(__file__).resolve().parent / "dist"

            launcher_path = exe_dir / "launcher.exe"

            if launcher_path.exists():
                print(f"Launching: {launcher_path}")
                subprocess.Popen([str(launcher_path)], cwd=str(launcher_path.parent), shell=False)
                sys.exit(0)
            else:
                print(f"[ERROR] launcher.exe not found at {launcher_path}")

    except Exception as e:
        print(f"[ERROR in check_and_update] {e}")
        traceback.print_exc()


    


# --- Full GoPro Automation Cycle ---
def run_gopro_cycle():
    latest_video = get_latest_video_file()
    if latest_video:
        local_video_file = download_video(latest_video)
        if local_video_file:
            video_link = upload_video_to_drive(local_video_file)
            if video_link:
                generate_qr_code(video_link)
    else:
        print("No latest video to upload.")

# --- Main Entry Point ---
if __name__ == "__main__":
    run_gopro_cycle()
    job_check_update()
    schedule.every().minute.do(job_check_update)

    print("Scheduler started: checking Slingshot.exe every minute.")
    print(f"Current version: {CheckLatestUpdate.get_local_version()}")

    while True:
        schedule.run_pending()
        time.sleep(1)



        


