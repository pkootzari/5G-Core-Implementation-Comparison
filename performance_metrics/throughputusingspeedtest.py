import time
import speedtest


def measure_throughput(repeats):
    st = speedtest.Speedtest()

    server_id = [60309]  # this is the information of the server: Bell Canada (Dorval, QC, Canada) [150.78 km]
    st.get_servers(server_id)
    
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
    
    print("download throughput: ")
    for throughput in download_throughput:
        print(throughput)
    
    print("upload throughput: ")
    for throughput in upload_throughput:
        print(throughput)

    