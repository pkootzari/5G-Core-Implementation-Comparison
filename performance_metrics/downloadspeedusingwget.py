import subprocess
import time
import os

def measure_download_speed(url, num_iterations):
    speeds = []

    for _ in range(num_iterations):
        start_time = time.time()
        # Run wget command and capture output
        result = subprocess.run(['wget', '--bind-address=10.45.0.2', url], capture_output=True, text=True)   # for downloading through the uesimtun0
        # result = subprocess.run(['wget', url], capture_output=True, text=True)                             # for downloading through the default network interface (without going through 5G core)
        end_time = time.time()

        
        # Calculate download speed (file size / download time)
        download_time = end_time - start_time
        download_speed = os.path.getsize(os.path.basename(url)) * 8 / download_time / 1024 / 1024 # Convert to Mbps
        print(download_speed)
        speeds.append(download_speed)

        # Remove the downloaded file
        os.remove(os.path.basename(url))

    return speeds

if __name__ == "__main__":
    url = 'https://go.dev/dl/go1.22.1.linux-amd64.tar.gz'                                   # Small file to measure download speed multiple times
    # url = "https://releases.ubuntu.com/20.04.6/ubuntu-20.04.6-live-server-amd64.iso"      # large file to measure the resource consupmtion on the 5G core VM
    num_iterations = 15  # Number of iterations

    speeds = measure_download_speed(url, num_iterations)

    print("Download Speeds (Mbps):")
    for speed in speeds:
        print(speed)