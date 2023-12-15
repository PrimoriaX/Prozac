import os
import re
import time
import requests
import zipfile
import shutil
import win32com.client
from colorama import Fore, init

init(autoreset=True)

ARDUINO_CLI_ZIP_URL = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"
ARDUINO_CLI_FILENAME = "arduino-cli.exe"
SKETCH_FILE = "mouse/mouse.ino"
BOARDS_TXT_LOCATION = os.path.expandvars("%LOCALAPPDATA%/Arduino15/packages/arduino/hardware/avr/1.8.6/boards.txt")


def download_and_extract_file(url, filename):
    print(Fore.GREEN + f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    with open(filename, "wb") as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall("./")
    print(Fore.GREEN + f"{filename} downloaded successfully.")


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


def cleanup_files(files, folders):
    print(Fore.YELLOW + "Cleaning up files...")

    for file in files:
        try:
            os.remove(file)
            print(Fore.GREEN + f"Deleted {file}")
        except Exception as e:
            print(Fore.RED + f"Failed to delete {file}. Error: {str(e)}")

    for folder in folders:
        try:
            shutil.rmtree(folder)
            print(Fore.GREEN + f"Deleted folder: {folder}")
        except Exception as e:
            print(Fore.RED + f"Failed to delete folder: {folder}. Error: {str(e)}")


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
    print(Fore.CYAN + "\nDetecting mice devices...")

    for idx, (name, vid, pid) in enumerate(mice, 1):
        print(f"{Fore.CYAN}{idx} →{Fore.RESET} {name}\tVID: {vid or 'Not found'}, PID: {pid or 'Not found'}")

    while True:
        try:
            choice = int(input("Select your mouse number: ")) - 1
            if choice in range(len(mice)):
                return mice[choice][1:]
            print(Fore.RED + "\nInvalid choice. Please try again.")
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")


def execute_cli_command(command):
    os.system(f"{ARDUINO_CLI_FILENAME} {command} >NUL 2>&1")


def main():
    download_and_extract_file(ARDUINO_CLI_ZIP_URL, "arduino-cli.zip")
    execute_cli_command("core install arduino:avr@1.8.6")
    execute_cli_command("lib install Mouse")
    vid, pid = user_select_mouse(list_mice_devices())
    update_boards_txt("0x" + vid, "0x" + pid)
    execute_cli_command(f"compile --fqbn arduino:avr:leonardo {SKETCH_FILE}")
    com_port = input(Fore.CYAN + "\nEnter your Arduino Leonardo COM port:")
    execute_cli_command(f"upload -p {com_port} --fqbn arduino:avr:leonardo {SKETCH_FILE}")
    cleanup_files(["arduino-cli.exe", "arduino-cli.zip", "LICENSE.txt", "README.md"], ["mouse"])


if __name__ == '__main__':
    main()
