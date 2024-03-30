import subprocess
import re

def ping(host, count):
    rtt_times = []
    try:
        ping_output = subprocess.check_output(
            ['ping', '-c', str(count), '-I', 'uesimtun0', host]
        )

        # ping_output = subprocess.check_output(
        #     ['ping', '-c', str(count), host]
        # )
        
        
        rtt_matches = re.findall(r'time=(\d+\.\d+)', ping_output.decode())
        if rtt_matches:
            rtt_times = [float(time) for time in rtt_matches]
    except subprocess.CalledProcessError:
        print('Error: Ping command failed.')
    return rtt_times

if __name__ == '__main__':
    host = '8.8.8.8'  
    count = 15 
    rtt_list = ping(host, count)
    if rtt_list:
        print("RTT times for each ICMP packet sent:")
        print(rtt_list)
    else:
        print('No RTT times received.')
