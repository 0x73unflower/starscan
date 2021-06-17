import socket
import threading
from queue import Queue
import subprocess
import sys
from datetime import datetime
import time
import platform
import os

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
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ Version 0.4
"""
)
time.sleep(0.5)

def main():
    try:
        remoteServer = input("Enter a remote host to scan: ")
        remoteServerIP = socket.gethostbyname(remoteServer)
        portRange = input("Enter port range: ")
    except socket.gaierror as e:
        print('Host name could not be resolved!')
        main()
    discoveredPorts = []

    print("-" * 67)
    print(f"[+] Scanning Target: {remoteServer}")
    print(f"[+] Scanning started at: {str(datetime.now())}")
    print("-" * 67)

    t1 = datetime.now()


    def scanner(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print(f"[+] Port {port}     Open")
                discoveredPorts.append(port)
            sock.close()
        except KeyboardInterrupt:
            print("[!] Exiting...")
        except socket.gaierror:
            print("[!] Hostname could not be resolved. Exiting...")
            sys.exit()

    def threader():
        while True:
            worker = q.get()
            scanner(worker)
            q.task_done()

    q = Queue()

    for i in range(500):
        t = threading.Thread(target=threader, daemon=True)
        t.start()

    # for worker in range(1, int(portRange)):
    #     q.put(worker)

    for worker in range(int(portRange)):
        q.put(worker)

    q.join()

    time.sleep(0.5)
    print("-" * 67)
    print(f'[+] Discovered Ports:')
    for port in discoveredPorts:
        print(f' - {port}')
    t2 = datetime.now()
    totalScanTime = t2 - t1
    print(f"\nThe scan took {totalScanTime}.")

    # Nmap

    # def nmap():
    #     try:
    #         nmapScan = input(f'Would you like to run a suggested scan on ports {discoveredPorts} (y/n): ')
    #         if nmapScan == 'y':
    #             cmd = 'nmap -p{port} -sC -sV -T4 {ip}'.format(port=','.join(discoveredPorts), ip=remoteServerIP)
    #             print(cmd)
    #             #Make a directory to write the found ports in NMAP
    #             #os.mkdir(f'{remoteServerIP} / STARSCAN')
    #             #os.chdir(remoteServerIP)
    #             os.system(cmd)
    #     except FileExistsError as e:
    #         print(e)
    #         exit()
    #     except Exception as noPorts:
    #         print('[!] No ports specified!', noPorts)
    # nmap()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('[!] Exiting...')
        quit()
