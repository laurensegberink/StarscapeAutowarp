# sasware autowarp
# v1.1

import pyautogui
import time
import threading
import keyboard
from notifypy import Notify
import colorama
from colorama import Fore
from ahk import AHK

start_exit = False

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
RESET = Fore.RESET

class Output: # definitely not pasted from my other project
    def Error(message : str):
        print(RED + "ERROR > " + message + colorama.Style.RESET_ALL)
    def Info(message : str):
        print(BLUE + "INFO > " + message + colorama.Style.RESET_ALL)
    def Success(message : str):
        print(GREEN + "SUCCESS > " + message + colorama.Style.RESET_ALL)

def Exit(Full : bool = False):
    global start_exit

    start_exit = True
    text_thread.join()

    if Full:
        print("Exiting...")
        exit()

    input("Press enter to exit...")
    exit()

try:
    ahk = AHK(executable_path = "AutoHotkeyU64.exe")
except:
    Output.Error(
        """AutoHotkeyU64.exe not found in same folder as script.
        Please download it from https://www.autohotkey.com/download/ahk.zip and place it in the same folder as this script."""
    )
    Exit()

current_text = "Waiting for Roblox to be active"
current_screen_dimensions = pyautogui.size()

def notify(title, message):
    notification = Notify()
    notification.title = title
    notification.message = message
    notification.send()

def is_image_on_screen(image):
    try:
        result = pyautogui.locateOnScreen(image, confidence=0.95, grayscale=False)
        return True and result != None
    except:
        return False

def can_warp():
    return is_image_on_screen('Speed.png') or is_image_on_screen('Speed2.png')

def get_center(Box):
    return (Box.left + Box.width // 2, Box.top + Box.height // 2)

def get_brightness(position):
    color = pyautogui.pixel(int(position[0]), int(position[1]))
    return sum(color) / 3

def warp():
    global current_text
    ahk.run_script("Send, {Space Up}")
    ahk.run_script("Send, {Space Down}")

    time.sleep(0.5)

    # Find position of the warp button (Destination.png)
    try:
        positions = pyautogui.locateAllOnScreen('Destination.png', confidence=0.9)
    except:
        notify("AutoWarp", "Destination reached!")
        exit()
    finally: # Possibly redundant?
        if positions == None:
            print("Destination not found")
            Exit(True)

    # Go through all positions and find the one that has the star color
    position = None
    for pos in positions:
        center = get_center(pos)
        color = pyautogui.pixel(int(center[0]), int(center[1]))
        if 70 > color[2] > 55:
            position = pos
            break

    if position == None:
        print("Destination not found")
        Exit(True)

    current_text = "Finding destination..."
    
    # Move mouse down until the brightness of the center pixel increases
    center = get_center(position)
    brightness = get_brightness(center)

    while True:
        ahk.run_script("mDown.ahk")
        new_brightness = get_brightness(center)
        if new_brightness > brightness:
            break
        brightness = new_brightness

    ahk.run_script("Send, {Space Up}")
    notify("AutoWarp", "Attempting to warp...")
    current_text = "Attempting to warp..."

    # Wait for Warping.png to show and then wait for it to disappear
    while not is_image_on_screen('Warping.png'):
        time.sleep(0.5)
    current_text = "Waiting for warp to finish..."
    while is_image_on_screen('Warping.png'):
        time.sleep(0.5)

print("[!] Waiting for Roblox to be active")
notify("AutoWarp", "Waiting for Roblox to be active")

if not ahk.find_window_by_title("Roblox"):
    print("Roblox is not open")
    Exit()

keyboard.add_hotkey('F6', Exit, args=[True])

while True:
    if ahk.find_window_by_title("Roblox") == ahk.get_active_window():
        break

import oGUI

top_text = oGUI.Text(oGUI.white, int(current_screen_dimensions[0] / 2), 50, 19, current_text)

def update_text():
    global start_exit
    while True:
        if start_exit:
            break
        oGUI.startLoop()
        top_text.x = int(current_screen_dimensions[0] / 2) - (len(current_text) * 6) + 100
        top_text.textStr = current_text
        top_text.draw()
        oGUI.endLoop()
        time.sleep(1/10)

oGUI.init()
text_thread = threading.Thread(target=update_text)
text_thread.start()

# Focus on Roblox
ahk.run_script("WinActivate, Roblox")
current_text = "Waiting for ship to be stationary..."

while True:

    time.sleep(0.5)

    if can_warp():
        print("Warping")
        warp()
        print("Warped")
        print("Waiting to warp...")
        current_text = "Waiting for next warp..."
        while not can_warp():
            time.sleep(0.5)
