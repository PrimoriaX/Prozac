import os, sys
import re
import time
import requests
import zipfile
import shutil
import win32com.client
import subprocess
from colorama import Fore, init

init(autoreset=True)

ARDUINO_CLI_ZIP_URL = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"
ARDUINO_CLI_FILENAME = "arduino-cli.exe"
SKETCH_FILE = "mouse/mouse.ino"
BOARDS_TXT_LOCATION = os.path.expandvars("%LOCALAPPDATA%/Arduino15/packages/arduino/hardware/avr/1.8.6/boards.txt")

def download_and_extract_file(url, filename):
    print(f"\n{Fore.LIGHTBLACK_EX}[{Fore.WHITE}x{Fore.LIGHTBLACK_EX}]{Fore.GREEN} Downloading Required Files...")
    response = requests.get(url, stream=True)
    with open(filename, "wb") as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall("./")

def update_boards_txt(vid, pid):
    pattern_to_replace = {
        "leonardo.build.vid=": vid,
        "leonardo.build.pid=": pid,
        ".vid=": vid,
        ".pid=": pid
    }

    with open(BOARDS_TXT_LOCATION, 'r') as file:
        data = file.readlines()

    for idx, line in enumerate(data):
        for pattern, replacement in pattern_to_replace.items():
            if pattern in line:
                prefix = line.split(pattern)[0]
                data[idx] = f"{prefix}{pattern}{replacement}\n"

    with open(BOARDS_TXT_LOCATION, 'w') as file:
        file.writelines(data)

def list_mice_devices():
    wmi = win32com.client.GetObject("winmgmts:")
    devices = wmi.InstancesOf("Win32_PointingDevice")
    mice_devices = []
    for device in devices:
        search_result = re.search(r'VID_(\w+)&PID_(\w+)', device.PNPDeviceID)
        if search_result:
            mice_devices.append((device.Name, *search_result.groups()))
        else:
            print(Fore.RED + f"No VID & PID found for device: {device.Name}")
    return mice_devices

def user_select_mouse(mice):
    print(f"\n{Fore.LIGHTBLACK_EX}[{Fore.WHITE}x{Fore.LIGHTBLACK_EX}]{Fore.GREEN} Detecting Mouse Devices...")

    for idx, (name, vid, pid) in enumerate(mice, 1):
        print(f"{Fore.GREEN}{idx} →{Fore.RESET} {name}\tVID: {vid or 'Not found'}, PID: {pid or 'Not found'}")

    while True:
        try:
            choice = int(input("Select your mouse number: ")) - 1
            if choice in range(len(mice)):
                return mice[choice][1:]
            print(Fore.RED + "\nInvalid choice. Please try again.")
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")

def execute_cli_command(command):
    process = subprocess.Popen(f"{ARDUINO_CLI_FILENAME} {command}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

def main():
    download_and_extract_file(ARDUINO_CLI_ZIP_URL, "arduino-cli.zip")
    execute_cli_command("core install arduino:avr@1.8.6")
    execute_cli_command("lib install Mouse")
    vid, pid = user_select_mouse(list_mice_devices())
    update_boards_txt("0x" + vid, "0x" + pid)
    execute_cli_command(f"compile --fqbn arduino:avr:leonardo {SKETCH_FILE}")
    
    com_port = input(f"\n{Fore.LIGHTBLACK_EX}[{Fore.WHITE}x{Fore.LIGHTBLACK_EX}]{Fore.GREEN} Enter your Arduino com port number (e.g. 3){Fore.RESET}: COM")
    ret_code, _, stderr = execute_cli_command(f"upload -p COM{com_port} --fqbn arduino:avr:leonardo {SKETCH_FILE}")
    
    if ret_code == 0:
        print(f"\n{Fore.LIGHTBLACK_EX}[{Fore.GREEN}Success{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Setup Completed!")
    else:
        print(f"\n{Fore.LIGHTBLACK_EX}[{Fore.RED}Error{Fore.LIGHTBLACK_EX}]{Fore.WHITE} Setup Failed. Please double check your com port number.")
    
    time.sleep(3)
    exit()

if __name__ == '__main__':
    main()
