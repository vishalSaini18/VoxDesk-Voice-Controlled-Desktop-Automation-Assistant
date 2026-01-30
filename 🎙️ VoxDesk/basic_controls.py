# basic_controls.py

import time
import webbrowser
import pyautogui
from datetime import datetime
import os
import sys
import pygetwindow as gw
import screen_brightness_control as sbc

# =========================
# KEYWORDS
# =========================

TIME_KEYWORDS = [
    "time",
    "current time",
    "what time is it",
    "what's the time",
    "what is the time",
    "tell me the time"
]

OPEN_GOOGLE_KEYWORDS = [
    "open google",
]

OPEN_YOUTUBE_KEYWORDS = [
    "open youtube",
    "launch youtube",
    "start youtube"
]

focus_search_PREFIX = ["search for"]

GOOGLE_SEARCH_PREFIX = ["search google for", "search on google for", "google search for", "google for" , "search google"]

SHUTDOWN_KEYWORDS = [
    "close all apps and shutdown",
    "close everything and shutdown",
    "shutdown pc completely",
    "force shutdown pc",
    "shutdown my pc",
    "shut down my pc",
    "shut down pc",
    "shutdown pc",
    "shutdown this pc"
]

maximize_window_keywords = [
    "fullscreen", "full screen", "maximize window", "maximize", "big screen"
]

go_forward_keywords = [
    "go forward", "go ahead", "forward"
]

restore_window_keywords = [
    "exit full screen", "minimize video", "small screen","restore"
]

CLOSE_TAB_KEYWORDS = [
    "close tab", "close this tab", "close this" "close it", 
    "exit tab", "close youtube", "stop youtube", "close the song"
]

close_active_window_keywords = [
    "close window", "close this window", "exit window", "close active window", "close"
]

press_button_prefix = ["press"]
Typing_prefix = ["type"]

BRIGHTNESS_UP_KEYWORDS = [
    "brightness up",
    "increase brightness",
    "brightness increase",
    "bright up"
]

BRIGHTNESS_DOWN_KEYWORDS = [
    "brightness down",
    "decrease brightness",
    "brightness decrease",
    "dim screen"
]

scroll_up_keywords = ["go up", "scroll up", "upar ja", "upar jaa", "upar", "up"]
scroll_down_keywords = ["go down", "scroll down", "neeche ja", "neeche jaa", "neeche", "down"]

left_click_keywords = ["left click", "left click here", "click here", "click"]
right_click_keywords = ["right click", "right click here"]

lock_screen_keywords = [
    "lock my screen",
    "lock the screen",
    "lock computer",
    "lock pc",
    "lock screen"
]

go_to_desktop_keywords = [
    "go to desktop",
    "show desktop",
    "desktop",
    "minimize all",
    "show me desktop"
]

# =========================
# FUNCTIONS
# =========================

def tell_time(speak):
    now = datetime.now().strftime("%I:%M %p")
    print(f"Current time: {now}")
    speak(f"The current time is {now}")

def open_google(speak):
    speak("Opening Google")
    webbrowser.open("https://www.google.com")

def open_youtube(speak):
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

def focus_search(command, speak):
    prefix = next(
        (p for p in focus_search_PREFIX if command.startswith(p)),
        None
    )

    if not prefix:
        return

    query = command.replace(prefix, "").strip()
    if not query:
        return

    speak(f"Searching for {query}")

    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.2)

    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    time.sleep(0.1)

    pyautogui.typewrite(query, interval=0.02)

def google_search(command, speak):
    prefix = next(
        (p for p in GOOGLE_SEARCH_PREFIX if command.startswith(p)),
        None
    )

    if not prefix:
        return

    query = command.replace(prefix, "").strip()
    if not query:
        return

    speak(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def shutdown_pc(speak):
    speak("Closing all applications and shutting down the computer")
    os.system("shutdown /s /f /t 3")
    sys.exit()

def maximize_window():
    time.sleep(0.2)
    win = gw.getActiveWindow()
    if win and not win.isMaximized:
        win.maximize()

def restore_window():
    time.sleep(0.2)
    win = gw.getActiveWindow()
    if win and win.isMaximized:
        win.restore()

def go_back():
    time.sleep(0.2)
    pyautogui.hotkey("alt", "left")

def go_forward():
    time.sleep(0.2)
    pyautogui.hotkey("alt", "right")

def next_tab():
    pyautogui.hotkey("ctrl", "tab")

def previous_tab():
    pyautogui.hotkey("ctrl", "shift", "tab")

def close_tab():
    pyautogui.hotkey("ctrl", "w")

# def press_button(command):
#     """
#     Press single key or multiple keys written as:
#     "tab tab tab enter"
#     """
#     if not command:
#         return

#     keys = command.strip().split()

#     for key in keys:
#         pyautogui.press(key)
#         time.sleep(0.05)

def press_button(command):
    if not command:
        return

    command = command.lower().replace("+", " plus ")
    tokens = command.split()

    groups = []
    current = []

    for token in tokens:
        if token == "plus":
            continue
        else:
            current.append(token)

            # end group when next token is not plus
            if tokens.index(token) == len(tokens) - 1 or tokens[tokens.index(token) + 1] != "plus":
                groups.append(current)
                current = []

    for group in groups:
        if len(group) == 1:
            pyautogui.press(group[0])
        else:
            pyautogui.hotkey(*group)

        time.sleep(0.1)

def type_basic(message):
    if not message:
        return

    # Type message
    pyautogui.typewrite(message, interval=0.03)

def close_active_window():
    time.sleep(0.2)
    pyautogui.hotkey("alt", "f4")

def _get_current_brightness():
    b = sbc.get_brightness()
    return b[0] if isinstance(b, list) else b

def brightness_up(step=10):
    current = _get_current_brightness()
    sbc.set_brightness(min(current + step, 100))

def brightness_down(step=10):
    current = _get_current_brightness()
    sbc.set_brightness(max(current - step, 0))

def scroll_up():
    pyautogui.scroll(250)  # scroll up

def scroll_down():
    pyautogui.scroll(-250)  # scroll down   

def left_click():
    pyautogui.click(button='left') 

def right_click():
    pyautogui.click(button='right')

def lock_screen():
    # speak("Locking the screen")
    os.system("rundll32.exe user32.dll,LockWorkStation")
    
def go_to_desktop():
    pyautogui.hotkey("win", "d")