import psutil
import time
import signal
import sys

# Define a signal handler function
def signal_handler(sig, frame):
    print("\nCtrl+C detected. Closing file and terminating.")
    # Close the file
    if 'file' in globals() and not file.closed:
        file.close()
    sys.exit(0)

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

def monitor_system_resources():
    
    # Get CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)

    # Get memory usage
    mem = psutil.virtual_memory()
    used_memory_mb = mem.used / (1024 * 1024)

    memory_file.write(str(used_memory_mb)+"\n")
    memory_file.flush()
    cpu_file.write(str(cpu_percent)+"\n")
    cpu_file.flush()

    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {used_memory_mb}")


try:
    # Open a file for writing
    memory_file = open("memory.txt", "w")
    cpu_file = open("cpu.txt", "w")

    # Main loop: write to the file every second
    while True:
        monitor_system_resources()
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    pass  # SIGINT will be caught by the signal handler
finally:
    # Close the file if it's open
    if 'file' in globals() and not file.closed:
        file.close()