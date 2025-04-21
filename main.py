import requests
from bs4 import BeautifulSoup
import os
import io
import qrcode
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import webbrowser
import urllib.parse
import platform
import subprocess
import json
import sys

def resource_path(filename):
    
    """ Get the absolute path to a resource, whether running from .py or from a PyInstaller .exe """
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        return os.path.join(sys._MEIPASS, filename)
    else:
        # Running in a normal Python environment
        return os.path.join(os.path.abspath("."), filename)

# Use it for loading config
with open(resource_path("config.json"), "r") as config_file:
    config = json.load(config_file)

# GoPro directory URL
GOPRO_BASE_URL = "http://10.5.5.9/videos/DCIM/100GOPRO/"
GOOGLE_DRIVE_FOLDER_ID = config["GOOGLE_DRIVE_FOLDER_ID"]  #Update GOOGLE_DRIVE_FOLDER_ID in config.json file.

# Set up Google Drive API service
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SERVICE_ACCOUNT_FILE = config["SERVICE_ACCOUNT_FILE"] #Update SERVICE_ACCOUNT_FILE in config.json file.

# Authenticate using service account credentials
creds = Credentials.from_service_account_file(resource_path(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)


def get_latest_video_file():
    try:
        # Fetch the HTML content of the directory
        response = requests.get(GOPRO_BASE_URL)

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all links in the directory listing (usually files will have <a> tags with href attributes)
            links = soup.find_all('a')

            # Filter links that end with ".MP4"
            video_files = [link.get('href') for link in links if link.get('href') and link.get('href').endswith('.MP4')]

            if video_files:
                # Sort video files based on their names (assuming they are sequentially numbered)
                latest_video = sorted(video_files, reverse=True)[0]  # Get the most recent file
                return latest_video
            else:
                print("No video files found in the directory.")
                return None
        else:
            print("Failed to connect to the GoPro.")
            return None
    except Exception as e:
        print(f"Error accessing the GoPro directory: {e}")
        return None


def download_video(latest_video):
    # Define the local filename for saving the video
    local_video_file = os.path.basename(latest_video)  # Extract filename (e.g., GX010185.MP4)

    # Construct the full local file path to save the video
    local_path = os.path.join(os.getcwd(), local_video_file)

    print(f"Downloading the latest video: {latest_video}")

    # ✅ Ensure latest_video does not already contain the full path
    if latest_video.startswith("/videos/"):
        video_url = f"http://10.5.5.9{latest_video}"  # Use full correct path
    else:
        video_url = f"{GOPRO_BASE_URL}{latest_video}"  # Append if needed

    print(f"Attempting to download from URL: {video_url}")

    # Download the video file
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
        # Extract the filename (e.g., GX010186.mp4)
        file_name = os.path.basename(local_video_file)

        # Prepare file metadata for Google Drive
        file_metadata = {
            'name': file_name,
            'parents': [GOOGLE_DRIVE_FOLDER_ID]
        }

        # Use resumable upload for large files
        media = MediaFileUpload(local_video_file, mimetype='video/mp4', resumable=True)
        request = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        )

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
    # Generate QR code for the video link
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(video_link)
    qr.make(fit=True)

    # Save the QR code image
    qr_image_path = os.path.abspath("video_qr_code.png")  # Absolute path
    img = qr.make_image(fill='black', back_color='white')
    img.save(qr_image_path)

    print(f"✅ QR Code saved at: {qr_image_path}")

    # Open the image using the system's default image viewer
    try:
        if platform.system() == "Windows":
            os.system(f'start "" "{qr_image_path}"')  # Works universally on Windows
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", qr_image_path], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", qr_image_path], check=True)

        print("✅ QR Code opened successfully.")
    except Exception as e:
        print(f"❌ Error opening QR Code: {e}")

    return qr_image_path
# Main execution flow
latest_video = get_latest_video_file()
if latest_video:
    local_video_file = download_video(latest_video)
    if local_video_file:
        video_link = upload_video_to_drive(local_video_file)
        if video_link:
            generate_qr_code(video_link)
else:
    print("No latest video to upload.")
