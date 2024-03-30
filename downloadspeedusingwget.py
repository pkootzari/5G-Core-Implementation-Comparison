import subprocess
import time
import os

def measure_download_speed(url, num_iterations):
    speeds = []

    for _ in range(num_iterations):
        start_time = time.time()
        # Run wget command and capture output
        result = subprocess.run(['wget', '--bind-address=10.60.0.6', url], capture_output=True, text=True)
        # result = subprocess.run(['wget', url], capture_output=True, text=True)
        end_time = time.time()

        
        # Calculate download speed (file size / download time)
        download_time = end_time - start_time
        download_speed = os.path.getsize(os.path.basename(url)) / download_time / 1024 / 1024  # Convert to Mbps
        print(download_speed)
        speeds.append(download_speed)

        # Remove the downloaded file
        os.remove(os.path.basename(url))

    return speeds

if __name__ == "__main__":
    # url = 'https://go.dev/dl/go1.22.1.linux-amd64.tar.gz'  # Replace with the URL of the file you want to download
    url = "https://releases.ubuntu.com/20.04.6/ubuntu-20.04.6-live-server-amd64.iso"
    num_iterations = 1  # Number of iterations

    speeds = measure_download_speed(url, num_iterations)

    print("Download Speeds (Mbps):")
    print(speeds)