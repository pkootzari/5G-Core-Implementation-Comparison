import time
import speedtest
import matplotlib.pyplot as plt

def measure_throughput(repeats):
    st = speedtest.Speedtest()
    
    download_throughput = []
    upload_throughput = []

    for _ in range(repeats):
        # Download speed measurement
        download_speed = st.download()
        download_throughput.append(download_speed / 1024 / 1024)  # Convert to Mbps

        # Upload speed measurement
        upload_speed = st.upload()
        upload_throughput.append(upload_speed / 1024/ 1024)  # Convert to Mbps
        print(download_speed/1024/1024, upload_speed/1024/1024)

        time.sleep(1)

    return download_throughput, upload_throughput

if __name__ == "__main__":
    download_throughput, upload_throughput = measure_throughput(15)
    print("download throughput: ", download_throughput)
    print("upload throguhput: ", upload_throughput)

    