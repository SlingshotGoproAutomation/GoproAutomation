# Singapore Polytechnic Intern 17/3/25 to 15/8/25

GoPro Video Auto Upload and QR Code Generator

This Executable file utilising Python automates the process of downloading the latest video from a GoPro camera, uploading it to Google Drive, and generating a QR code for easy access.

<====Features=====>

-> Automatically fetches the latest video from the GoPro camera.

-> Downloads the video to an automatically generated folder e.g. 12/3/25.

->Uploads the video to Google Drive using a service account (no user login required).

->Generates a QR code for the Google Drive link.

-> Opens the QR code in the system's default image viewer for easy scanning.

->Scans for latest version of exe file.

->Automatically downloads and replaces the old exe file.

->Automatically creates desktop shortcut for the new exe file.

<====Requirements=====>

-> A USB WIFI Adaptor connected to the Gopro camera wifi.

-> A Google Drive service account with a valid 'service_account.json' key file.

<====Hardware Installation=====>

-> Install Gopro Quikk on your tablet/phone.

-> Connect the Gopro camera to your tablet/phone using bluetooth.

-> Press Enable Preview in the app to enable WIFI Hotspot from the Gopro. #When GoPro battery is <=20%, the WIFI hotspot feature is disabled.

-> Place your GoPro camera on the same network as your computer by:

-> Open control panel on your computer->Network & internet -> Network & Sharing -> Change Adaptor Settings.

-> Right click on the USB WIFI Adaptor, and press Connect/Disconnect.

-> Connect the USB WIFI Adaptor to the Gopro WIFI. Gopro password can be found on the Gopro Quikk app.

-> The inbuilt USB WIFI Adaptor on your computer should be connected to the local WIFI network at your premises.

<====Software Installation=====>

Step 1: Create a Google Drive Service Account

->Go to Google Cloud Console → * https://console.cloud.google.com/

->Under Quick Access -> APIs & Services ->Enable APIs and services -> Search for Google Drive API -> Enable.

->Select your project (or create a new one).

->Go to IAM & Admin → Service Accounts → Create Service Account.

->Give it a name (e.g., gopro-uploader).

->Under "Grant this service account access to project", assign:

->"Editor" role (or "Owner" for full control).

->Click Continue → Done.

Step 2: Download the JSON Key File

->In the Service Accounts list, find your new account.

->Click on it → Go to the "Keys" tab.

->Click "Add Key" → "Create New Key" → Select JSON.

->Download and save this file (e.g., service_account.json) in your project folder.

Ensure that this file is named as service_account.json.

Step 3: Share a Google Drive Folder with the Service Account.

->Go to Google Drive.

->Create a new folder (e.g., "GoPro Uploads").

->Right-click → Share → Add the Service Account's email (xxxx@xxxx.iam.gserviceaccount.com).

->Set it as Editor (so it can upload files).

-> Change the Sharing Permissions to: Anyone with the link can view. 

Copy your Google Drive service account JSON file to the project directory and update the script accordingly.

Step 4: Download the latest release executable file Slingshot.exe.

-> Go to the repository GoProAutomation -> Click on Releases at right side of screen -> Download Slingshot.exe with the tag "latest".

Step 5: Download the latest release executable file launcher.exe .

-> Go to the repository GoProAutomation -> Click on Releases at right side of screen -> Download launcher.exe with the tag "latest".

Step 6: Configuration

Update the following variables in 'config.json':

-> GOOGLE_DRIVE_FOLDER_ID = "your-google-drive-folder-id" #e.g. https://drive.google.com/drive/folders/**FOLDER ID**

-> SERVICE_ACCOUNT_FILE = "service_account.json" # Your service account key file

->Ensure that the files config.json and service_account.json are present in the project directory:


<====Usage=====>

The script will:

->Fetch the latest video from the GoPro.

->Downloads the video to an automatically generated folder e.g. 12/3/25.

->Uploads the video to Google Drive using a service account (no user login required).

->Generate and open a QR code to access the video.

->Scans for latest version of exe file.

->Automatically downloads and replaces the old exe file.

->Automatically creates desktop shortcut for the new exe file.

<====Playing video on local machine=====>

Download VLC media player, and set all videos to always play using VLC Media Player.

This prevents codec error, where video does not play but audio plays.

<====Troubleshooting=====>

If GoPro is powered off, the Gopro WIFI will have to be re-connected to the USB WIFI Adaptor. "Enable Preview" must also be clicked on the Gopro Quikk App to restart the WIFI hotspot.

If the GoPro video list does not update, try restarting the camera.

Ensure the 'service_account.json' file is correct and has the necessary permissions.

If video cannot be accessed by QR code, ensure that the Google Drive folder's sharing permissions are set to: "Anyone with the link can view". 

If the executable file Slingshot.exe is unable to run succesfully, ensure that the required files such as config.json and service_account.json are included in the same project directory.

If the QR code does not open, check your system's default image viewer settings.
