import pyautogui
import time
import pygetwindow as gw
import webbrowser
import pywhatkit
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from speech_engine import speak
# -------------------------------
#  KEYWORD GROUPS
# -------------------------------

PLAY_SONG_PREFIX = "play"

PAUSE_KEYWORDS = [
    "pause", "pause it",  
    "pause the music", "pause song", "stop music", 
    "pause video", "stop the song", "hold on", 
    "mute", "mute it", "stop the video", "stop playing", "stop video"
]

PLAY_KEYWORDS = [
    "resume", "play", "continue", "play it", "start playing"
]

REWIND_KEYWORDS = [
    "rewind", "back 10 seconds", 
    "back little", "rewind a bit"
]

FORWARD_KEYWORDS = [
    "forward", "skip", "ahead", "jump", 
    "go forward", "forward 10 seconds"
]

NEXT_VIDEO_KEYWORDS = [
    "next video", "skip video", "play next", "next", "play next video", "play next song"
]

PREVIOUS_VIDEO_KEYWORDS = [
    "previous video", "last video", "go back video", 
]

# -------------------------------
#  CONTROL FUNCTIONS
# -------------------------------
def get_active_window():
    try:
        return gw.getActiveWindow()
    except:
        return None

def activate_youtube_tab():
    """
    Ensure Chrome is active, then bring any YouTube tab to front.
    Returns True if successful.
    """

    # STEP 0 — Ensure Chrome window is active
    if not activate_chrome():
        return False

    time.sleep(0.2)

    # STEP 1 — Try to activate existing YouTube tab
    for win in gw.getWindowsWithTitle("YouTube"):
        try:
            if win.isMinimized:
                win.restore()

            win.activate()
            time.sleep(0.3)

            active = gw.getActiveWindow()
            if active and "youtube" in active.title.lower():
                return True
        except:
            pass

    return False

def restore_window(win):
    try:
        if win:
            win.activate()
    except:
        pass




def play_song_command(command, speak, play_song_in_same_tab):
    song = (
        command.replace(PLAY_SONG_PREFIX, "")
        .replace("on youtube", "")
        .strip()
    )

    if not song:
        return

    speak(f"Playing {song}")
    play_song_in_same_tab(song)

def pause_video():
    prev = get_active_window()

    if activate_chrome() and switch_to_youtube_tab():
        time.sleep(0.2)
        pyautogui.press("k")

    time.sleep(0.2)
    restore_window(prev)

def play_video():
    prev = get_active_window()

    if activate_chrome() and switch_to_youtube_tab():
        time.sleep(0.2)
        pyautogui.press("k")

    time.sleep(0.2)
    restore_window(prev)

def rewind_video():
    prev = get_active_window()

    if activate_chrome() and switch_to_youtube_tab():
        time.sleep(0.2)
        pyautogui.press("j")

    time.sleep(0.2)
    restore_window(prev)

def forward_video():
    prev = get_active_window()

    if activate_chrome() and switch_to_youtube_tab():
        time.sleep(0.2)
        pyautogui.press("l")

    time.sleep(0.2)
    restore_window(prev)

def next_video():
    prev = get_active_window()

    if activate_chrome() and switch_to_youtube_tab():
        time.sleep(0.2)
        pyautogui.hotkey("shift", "n")

    time.sleep(0.2)
    restore_window(prev)

def previous_video():
    prev = get_active_window()

    if activate_chrome() and switch_to_youtube_tab():
        time.sleep(0.2)
        pyautogui.hotkey("shift", "p")

    time.sleep(0.2)
    restore_window(prev)

# def activate_chrome():
#     """Activate Chrome safely and maximize only if needed (no flicker)."""

#     try:
#         active = gw.getActiveWindow()
#         if active and "chrome" in active.title.lower():
#             # Chrome already active → just ensure maximized
#             try:
#                 if not active.isMaximized:
#                     active.maximize()
#             except:
#                 pass
#             return True
#     except:
#         pass

#     for win in gw.getWindowsWithTitle("Chrome"):
#         try:
#             # Restore only if minimized
#             if win.isMinimized:
#                 win.restore()
#                 time.sleep(0.2)

#             win.activate()
#             time.sleep(0.2)

#             # Maximize ONLY if not already maximized
#             try:
#                 if not win.isMaximized:
#                     win.maximize()
#             except:
#                 pass

#             return True
#         except:
#             pass

#     return False


CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def activate_chrome():
    """Activate Chrome safely. Open it if closed."""

    # 1️⃣ If Chrome already active
    try:
        active = gw.getActiveWindow()
        if active and "chrome" in active.title.lower():
            if not active.isMaximized:
                active.maximize()
            return True
    except:
        pass

    # 2️⃣ If Chrome running but not active
    for win in gw.getWindowsWithTitle("Chrome"):
        try:
            if win.isMinimized:
                win.restore()
                time.sleep(0.2)

            win.activate()
            time.sleep(0.2)

            if not win.isMaximized:
                win.maximize()

            return True
        except:
            pass

    # 3️⃣ Chrome not running → START IT
    try:
        subprocess.Popen(CHROME_PATH)
        time.sleep(1.5)

        for win in gw.getWindowsWithTitle("Chrome"):
            try:
                win.activate()
                if not win.isMaximized:
                    win.maximize()
                return True
            except:
                pass
    except:
        pass

    return False

def chrome_is_active():
    try:
        active = gw.getActiveWindow()
        return active and "chrome" in active.title.lower()
    except:
        return False

def switch_to_youtube_tab():
    # 1️⃣ Check if Chrome exists
    chrome_windows = gw.getWindowsWithTitle("Chrome")
    if not chrome_windows:
        return False  # ExitApp, 1

    # 2️⃣ Activate Chrome
    try:
        chrome = chrome_windows[0]
        if chrome.isMinimized:
            chrome.restore()
        chrome.activate()
    except:
        return False

    time.sleep(0.3)

    # 3️⃣ Ctrl + Shift + A
    pyautogui.hotkey("ctrl", "shift", "a")
    time.sleep(0.4)

    # 4️⃣ Type "youtube"
    pyautogui.typewrite("www.youtube.com", interval=0.02)
    time.sleep(0.4)

    # 5️⃣ Press Enter
    pyautogui.press("enter")
    time.sleep(0.6)

    # 6️⃣ Check active window title
    active = gw.getActiveWindow()
    if active and "youtube" in active.title.lower():
        return True   # ExitApp, 0
    else:
        return False  # ExitApp, 1


def play_song_in_same_tab(song):
    url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"

    # STEP 1 — Ensure Chrome exists
    if not activate_chrome():
        webbrowser.open("https://www.youtube.com")
        time.sleep(4)
        activate_chrome()

    time.sleep(0.4)

    # STEP 2 — Try switching to existing YouTube tab
    youtube_found = switch_to_youtube_tab()
    time.sleep(0.4)

    # STEP 3 — If NO YouTube tab → open NEW tab AND load YouTube
    if not youtube_found:
        pyautogui.hotkey("ctrl", "t")
        time.sleep(0.3)
        # pyautogui.typewrite("https://www.youtube.com", interval=0.02)
        pyautogui.press("enter")

        # wait for YouTube to actually load
        start = time.time()
        while time.time() - start < 10:
            try:
                active = gw.getActiveWindow()
                if active and "youtube" in active.title.lower():
                    break
            except:
                pass
            time.sleep(0.4)

    # STEP 4 — FINAL safety check
    try:
        active = gw.getActiveWindow()
        if not active or "chrome" not in active.title.lower():
            webbrowser.open(url)
            return
    except:
        webbrowser.open(url)
        return

    # STEP 5 — Search INSIDE YouTube tab
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.2)
    pyautogui.typewrite(url, interval=0.02)
    pyautogui.press("enter")

    # STEP 6 — Wait for results
    time.sleep(3)

    # STEP 7 — Click first video
    screen_w, screen_h = pyautogui.size()
    x = int(screen_w * 0.35)   # left-shifted
    y = int(screen_h * 0.45)
    pyautogui.click(x, y)


def wait_for_video_visible(timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        loc = pyautogui.locateOnScreen(
            "yt_thumb.png",
            confidence=0.7
        )
        if loc:
            return True
        time.sleep(0.5)
    return False


# def play_song_in_same_tab(song):
#     url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"

#     # STEP 1 — Ensure Chrome exists
#     if not activate_chrome():
#         webbrowser.open("https://www.youtube.com")
#         time.sleep(4)
#         activate_chrome()

#     time.sleep(0.4)

#     # STEP 2 — Try switching to existing YouTube tab
#     youtube_found = switch_to_youtube_tab()
#     time.sleep(0.4)

#     # STEP 3 — If NO YouTube tab → open NEW tab AND load YouTube
#     if not youtube_found:
#         pyautogui.hotkey("ctrl", "t")
#         time.sleep(0.3)
#         # pyautogui.typewrite("https://www.youtube.com", interval=0.02)
#         pyautogui.press("enter")

#         # wait for YouTube to actually load
#         start = time.time()
#         while time.time() - start < 10:
#             try:
#                 active = gw.getActiveWindow()
#                 if active and "youtube" in active.title.lower():
#                     break
#             except:
#                 pass
#             time.sleep(0.4)

#     # STEP 4 — FINAL safety check
#     try:
#         active = gw.getActiveWindow()
#         if not active or "chrome" not in active.title.lower():
#             webbrowser.open(url)
#             return
#     except:
#         webbrowser.open(url)
#         return

#     # STEP 5 — Search INSIDE YouTube tab
#     pyautogui.hotkey("ctrl", "l")
#     time.sleep(0.2)
#     pyautogui.typewrite(url, interval=0.02)
#     pyautogui.press("enter")

#     # STEP 6 — Wait until video visible (NO selenium)
#     if not wait_for_video_visible():
#         speak("Song did not load in time.")
#         return


#     # STEP 7 — Click first video
#     screen_w, screen_h = pyautogui.size()
#     x = int(screen_w * 0.35)   # left-shifted
#     y = int(screen_h * 0.45)
#     pyautogui.click(x, y)