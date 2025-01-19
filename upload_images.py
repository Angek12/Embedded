import os
import time
import subprocess
import shutil

MONITOR_FOLDER = "./camera_folder"  #Camera saves 
UPLOADED_FOLDER = "./uploaded"  #Uploaded pictures
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
UPLOAD_ATTRIBUTE = "imageFile"
CHECK_INTERVAL = 5  #Check the folder (in seconds)
UPLOAD_DELAY = 30  # Time delay before attempting to upload a file (in seconds)

os.makedirs(UPLOADED_FOLDER, exist_ok=True)

def upload_file(file_path):
    """Uploads a file using the curl command."""
    try:
        command = [
            "curl", "-X", "POST",
            "-F", f"{UPLOAD_ATTRIBUTE}=@{file_path}",
            UPLOAD_URL
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0 and "success" in result.stdout.lower():
            print(f"[INFO] Successfully uploaded: {file_path}")
            return True
        else:
            print(f"[ERROR] Failed to upload {file_path}: {result.stderr or result.stdout}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception while uploading {file_path}: {e}")
        return False

while True:
    try:
        #all files in the monitor folder
        files = sorted(os.listdir(MONITOR_FOLDER))
        for file_name in files:
            file_path = os.path.join(MONITOR_FOLDER, file_name)

            # Skip files that are not images
            if not os.path.isfile(file_path) or not file_name.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            # Wait before attempting upload
            time.sleep(UPLOAD_DELAY)

            # Upload the file
            if upload_file(file_path):
                # Move the file to the "uploaded" folder
                destination_path = os.path.join(UPLOADED_FOLDER, file_name)
                shutil.move(file_path, destination_path)
                print(f"[INFO] Moved {file_name} to uploaded folder.")

    except Exception as e:
        print(f"[ERROR] Exception in main loop: {e}")

    # Wait before checking the folder again
    time.sleep(CHECK_INTERVAL)
