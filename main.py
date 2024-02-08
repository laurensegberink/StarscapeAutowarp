import pyautogui
import time
import sys
import threading
import keyboard
from ahk import AHK

ahk = AHK(executable_path="AutoHotkeyU64.exe")

current_text = "Waiting for Roblox to be active"
current_screen_dimensions = pyautogui.size()

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
    positions = pyautogui.locateAllOnScreen('Destination.png', confidence=0.9)
    if positions == None:
        print("Destination not found")
        sys.exit(1)

    # Go through all positions and find the one that has the star color
    position = None
    for pos in positions:
        center = get_center(pos)
        color = pyautogui.pixel(int(center[0]), int(center[1]))
        if 70 > color[2] > 55:
            position = pos
            break

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
    current_text = "Attempting to warp..."
    # If X is pressed in the next 3 seconds, close the program
    hotkeyobject = keyboard.add_hotkey('x', lambda: sys.exit(0))
    time.sleep(3)
    keyboard.remove_hotkey(hotkeyobject)

    # Wait for Warping.png to show and then wait for it to disappear
    while not is_image_on_screen('Warping.png'):
        time.sleep(0.5)
    current_text = "Waiting for warp to finish..."
    while is_image_on_screen('Warping.png'):
        time.sleep(0.5)

print("Waiting for Roblox to be active")

while True:
    if ahk.find_window_by_title("Roblox") == ahk.get_active_window():
        break

import oGUI

top_text = oGUI.Text(oGUI.white, int(current_screen_dimensions[0] / 2), 50, 19, current_text)

def update_text():
    while True:
        oGUI.startLoop()
        top_text.x = int(current_screen_dimensions[0] / 2) - (len(current_text) * 6)
        top_text.textStr = current_text
        top_text.draw()
        oGUI.endLoop()
        time.sleep(1/20)

oGUI.init()
threading.Thread(target=update_text).start()

# Focus on Roblox
ahk.run_script("WinActivate, Roblox")

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