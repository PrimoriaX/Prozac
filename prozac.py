import cv2
import numpy as np
import pyautogui
import win32api
import serial
import mss
import time

from colorama import Fore, Style

#Settings
COM_PORT = "COM3"
X_FOV = 100
Y_FOV = 100
AIM_KEY = 0x02
TRIGGER_KEY = 0x12
X_SPEED = 3
Y_SPEED = 3
AIM_OFFSET = 7
LOWER_COLOR = [140, 120, 180]
UPPER_COLOR = [160, 200, 255]
#Settings

class Prozac:
    def __init__(self):
        self.mouse = Mouse()
        self.capture = Capture()
    
    def listen(self):
        while True:
            if win32api.GetAsyncKeyState(AIM_KEY) < 0:
                self.run("aim")
            if win32api.GetAsyncKeyState(TRIGGER_KEY) < 0:
                self.run("click")

            time.sleep(0.008)
                
    def run(self, task):
        hsv = cv2.cvtColor(self.capture.get_screen(), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array(LOWER_COLOR), np.array(UPPER_COLOR))
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if contours:
            screen_center = (X_FOV // 2, Y_FOV // 2)
            min_distance = float('inf')
            closest_contour = None

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w // 2, y + h // 2)
                distance = ((center[0] - screen_center[0]) ** 2 + (center[1] - screen_center[1]) ** 2) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    closest_contour = contour

            x, y, w, h = cv2.boundingRect(closest_contour)
            cX = x + w // 2
            top_most_y = y + AIM_OFFSET

            x_offset = cX - screen_center[0]
            y_offset = top_most_y - screen_center[1]

            if task == "aim":
                self.mouse.move(x_offset * (X_SPEED * 0.1), y_offset * (Y_SPEED * 0.1))

            if task == "click":
                if abs(x_offset) <= 3 and abs(y_offset) <= 7:
                    self.mouse.click()

class Mouse:
    def __init__(self):
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 115200
        self.serial_port.timeout = 0
        self.serial_port.port = COM_PORT
        try:
            self.serial_port.open()
            print(f"{Fore.GREEN}\t\t\t\t\b\b{Fore.LIGHTBLACK_EX}[{Fore.GREEN}SUCCESS{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} Connected to Arduino Leonardo on '{COM_PORT}'!")
        except serial.SerialException:
            print(f"{Fore.RED}\t\t[ERROR]{Style.RESET_ALL} Failed to connect because the specified COM port was not found, exiting...")
            time.sleep(10)

    def move(self, x, y):
        self.serial_port.write(f'{x},{y}\n'.encode())

    def click(self):
       self.serial_port.write('CLICK\n'.encode())

class Capture:
    def __init__(self):
        monitor_size = pyautogui.size()
        self.region = self.calculate_region(monitor_size)

    def calculate_region(self, monitor_size):
        x_center = monitor_size.width // 2
        y_center = monitor_size.height // 2
        left = x_center - X_FOV // 2
        top = y_center - Y_FOV // 2
        width = X_FOV
        height = Y_FOV
        return {'left': left, 'top': top, 'width': width, 'height': height}

    def get_screen(self):
        with mss.mss() as sct:
            screenshot = sct.grab(self.region)
            return np.array(screenshot)
