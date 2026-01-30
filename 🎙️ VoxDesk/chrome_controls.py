import pyautogui
import time
import pygetwindow as gw
import webbrowser
import pywhatkit
import subprocess
import os
from youtube_controls import activate_chrome
from speech_engine import speak

VOLUME_UP_KEYWORDS = [
    "volume up", "increase volume", "louder", 
    "sound up", "increase sound"
]

VOLUME_DOWN_KEYWORDS = [
    "volume down", "decrease volume", "lower volume", 
    "quiet", "reduce sound","reduce volume"
]

open_new_tab_keywords = [
    "open new tab",  "new tab", "open tab"
]

search_in_browser_prefix = ["search", "search in browser for", "search browser for", "search for in browser"]

activate_chrome_keywords = ["activate chrome",
        "open chrome",
        "bring chrome",
        "switch to chrome",
        "focus chrome"
        ]

# -------------------------------
#  CHROME TAB CONTROLS
# -------------------------------


# def volume_down():
#     pyautogui.press("volumedown")

# def volume_up():
#     pyautogui.press("volumeup")

def volume_up(times=1):
    for _ in range(times):
        pyautogui.press("volumeup")

def volume_down(times=1):
    for _ in range(times):
        pyautogui.press("volumedown")

def activate_chrome_cmd():
    return activate_chrome()

def open_new_tab():
    if activate_chrome():
        time.sleep(0.15)
        pyautogui.hotkey("ctrl", "t")
        return True
    return False

def search_in_browser(command):
    prefix = next(
        (p for p in search_in_browser_prefix if command.startswith(p)),
        None
    )

    if not prefix:
        return

    query = command.replace(prefix, "").strip()
    if not query:
        return

    speak(f"Searching for {query}")

    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.2)

    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    time.sleep(0.1)

    pyautogui.typewrite(query, interval=0.02)
    pyautogui.press("enter")
