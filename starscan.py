# Add a text to write to
# Set up threading +
# Add options to scan individual ports
# Nmap intergration
# Set up arguments

import socket
import threading
from queue import Queue
import subprocess
import sys
from datetime import datetime
import time
import platform

if platform.system() == "Windows":
    subprocess.call("cls", shell=True)
else:
    subprocess.call("clear", shell=True)

print(
    """
███████╗████████╗ █████╗ ██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗            
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║            
███████╗   ██║   ███████║██████╔╝███████╗██║     ███████║██╔██╗ ██║            
╚════██║   ██║   ██╔══██║██╔══██╗╚════██║██║     ██╔══██║██║╚██╗██║            
███████║   ██║   ██║  ██║██║  ██║███████║╚██████╗██║  ██║██║ ╚████║            
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ Version 0.2
"""
)
time.sleep(0.5)

remoteServer = input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)
portRange = input("Enter port range: ")

print("-" * 67)
print(f"[+] Scanning Target: {remoteServer}")
print(f"[+] Scanning started at: {str(datetime.now())}")
print("-" * 67)

t1 = datetime.now()


def main(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print(f"[+] Port {port}     Open")
        sock.close()
    except KeyboardInterrupt:
        print("[!] Exiting...")
    except socket.gaierror:
        print("[!] Hostname could not be resolved. Exiting...")
        sys.exit()

def threader():
    while True:
        worker = q.get()
        main(worker)
        q.task_done()

q = Queue()

for i in range(10000):
    t = threading.Thread(target=threader, daemon=True)
    t.start()

for worker in range(1, int(portRange)):
    q.put(worker)

q.join()

t2 = datetime.now()
totalScanTime = t2 - t1
print(f"\nThe scan took {totalScanTime}.")

if __name__ == "__main__":
    main(65535)
