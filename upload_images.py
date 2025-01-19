import os
import time
import shutil
import subprocess

# Configuration
camera_folder = "C:\\Users\\Kevine\\Documents\\Embedded\\Embedded work\\camera_folder"  # Folder where the camera saves images
uploaded_folder = "C:\\Users\\Kevine\\Documents\\Embedded\\Embedded work\\uploaded_folder"  # Folder to store uploaded images
upload_url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
upload_key = "imageFile"
check_interval = 30  # Check interval in seconds

# Ensure the uploaded folder exists
os.makedirs(uploaded_folder, exist_ok=True)


def upload_image(file_path):
    """
    Upload an image using the curl command.
    Args:
        file_path (str): Full path to the image file.

    Returns:
        bool: True if the upload is successful, False otherwise.
    """
    try:
        # Prepare the curl command
        command = [
            "curl",
            "-X", "POST",
            "-F", f"{upload_key}=@{file_path}",
           upload_url
        ]
        # Execute the curl command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check the response for success
        if result.returncode == 0 and "success" in result.stdout.lower():
            print(f"Successfully uploaded: {file_path}")
            return True
        else:
            print(f"Failed to upload {file_path}: {result.stderr or result.stdout}")
            return False
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")
        return False


def monitor_folder():
    """
    Monitor the camera folder for new images and upload them.
    """
    while True:
        # Get the list of files in the camera folder
        files = [f for f in os.listdir(camera_folder) if os.path.isfile(os.path.join(camera_folder, f))]

        for file_name in files:
            file_path = os.path.join(camera_folder, file_name)

            # Attempt to upload the image
            if upload_image(file_path):
                # Move the uploaded file to the uploaded folder
                uploaded_path = os.path.join(uploaded_folder, file_name)
                shutil.move(file_path, uploaded_path)
                print(f"File moved to uploaded folder: {uploaded_path}")
            else:
                print(f"Upload failed. File remains in the folder: {file_path}")

        # Wait before checking the folder again
        time.sleep(check_interval)


if __name__ == "__main__":
    try:
        print("Monitoring folder for new images...")
        monitor_folder()
    except KeyboardInterrupt:
        print("\nStopped monitoring.")