# Singapore Polytechnic Intern 17/3/25 to 15/8/25

GoPro Video Auto Upload and QR Code Generator

This Python script automates the process of downloading the latest video from a GoPro camera, uploading it to Google Drive, and generating a QR code for easy access.

<====Features=====>

-> Automatically fetches the latest video from the GoPro camera.

-> Downloads the video to the local system.

->Uploads the video to Google Drive using a service account (no user login required).

->Generates a QR code for the Google Drive link.

-> Opens the QR code in the system's default image viewer for easy scanning.

<====Requirements=====>

-> A USB WIFI Adaptor connected to the Gopro camera wifi.

-> A Google Drive service account with a valid 'service_account.json' key file.

-> Python 3.6+ installed with the required dependencies.

<====Hardware Installation=====>

-> Install Gopro Quikk on your tablet/phone. 

-> Connect the Gopro camera to your tablet/phone using bluetooth. 

-> Press Enable Preview in the app to enable WIFI Hotspot from the Gopro.

-> Place your GoPro camera on the same network as your computer by:

-> Open control panel on your computer->Network & internet -> Network & Sharing -> Change Adaptor Settings.

-> Right click on the USB WIFI Adaptor, and press Connect/Disconnect. 

-> Connect the USB WIFI Adaptor to the Gopro WIFI. Gopro password can be found on the Gopro Quikk app.

-> The inbuilt USB WIFI Adaptor on your computer should be connected to the local WIFI network at your premises.

<====Software Installation=====>

Step 1: Download Python from python.org and install it.

-> During installation, check the box that says "Add Python to PATH".

->Install pip manually

->Open Command Prompt and type:

* *python -m ensurepip --default-pip* *

-> Verify pip Installation

->After installation, check again:
Type in command prompt: pip --version

Step 2: Download and Install Git

->Download Git from the official website:

👉 * *https://git-scm.com/downloads* *

-> Run the installer and follow these steps:

-> Keep clicking Next until you reach the Adjusting your PATH environment option.

-> Select: ✅ "Git from the command line and also from 3rd-party software."

-> Click Next and complete the installation.

->Verify Git Installation

->Open Command Prompt (cmd) or PowerShell.

-> Type the following command and press Enter:

* *git --version* *

✅ If installed correctly, you'll see a version number, like:

* *git version 2.x.x* *

Step 3: Create a Google Drive Service Account

->Go to Google Cloud Console → * *https://console.cloud.google.com/* *

->Select your project (or create a new one).

->Go to IAM & Admin → Service Accounts → Create Service Account.

->Give it a name (e.g., gopro-uploader).

->Under "Grant this service account access to project", assign:

->"Editor" role (or "Owner" for full control).

->Click Continue → Done.

Step 4:  Download the JSON Key File

->In the Service Accounts list, find your new account.

->Click on it → Go to the "Keys" tab.

->Click "Add Key" → "Create New Key" → Select JSON.

->Download and save this file (e.g., service_account.json) in your project folder.

Step 5: Share a Google Drive Folder with the Service Account.

->Go to Google Drive.

->Create a new folder (e.g., "GoPro Uploads").

->Right-click → Share → Add the Service Account's email (xxxx@xxxx.iam.gserviceaccount.com).

->Set it as Editor (so it can upload files).

->Run the following command in command prompt:

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

->Clone this repository in command prompt:

* *git clone https://github.com/SlingshotGoproAutomation/GoproAutomation.git* *

This command clones (downloads) the repository from GitHub to your local computer.

-> Create requirements.txt Manually

->Open Notepad (Windows) or TextEdit (Mac).

-> Add the following lines:

* *requests* *

* *beautifulsoup4* *

* *qrcode* *

* *google-api-python-client* *

* *google-auth* *

* *google-auth-oauthlib* *

* *google-auth-httplib2* *


-> Save the file as requirements.txt inside your project folder (search Gopro Automation in file explorer).

-> Run the install command again:

* *pip install -r requirements.txt* *

Copy your Google Drive service account JSON file to the project directory and update the script accordingly.


<====Configuration=====>

Update the following variables in 'main.py':

GOPRO_BASE_URL = * *"http://10.5.5.9/videos/DCIM/100GOPRO/"* *

GOOGLE_DRIVE_FOLDER_ID = * *"your-google-drive-folder-id"* * #e.g. https://drive.google.com/drive/folders/**FOLDER ID**

SERVICE_ACCOUNT_FILE = * *"service_account.json"* *  # Your service account key file

<====Usage=====>

->Open Command Prompt (cmd).

Type: python
or python3

-> A Python interactive shell should open. You can now type Python code directly:

-> To exit, type:

exit()

Run the script:
python main.py
The script will:

->Fetch the latest video from the GoPro.

->Download it to the local machine.

->Upload it to Google Drive.

->Generate and open a QR code to access the video.

<====Troubleshooting=====>

If GoPro is powered off, the Gopro WIFI will have to be re-connected to the USB WIFI Adaptor. "Enable Preview" must also be clicked on the Gopro Quikk App to restart the WIFI hotspot.

If the GoPro video list does not update, try restarting the camera.

Ensure the 'service_account.json' file is correct and has the necessary permissions.

If the QR code does not open, check your system's default image viewer settings.
