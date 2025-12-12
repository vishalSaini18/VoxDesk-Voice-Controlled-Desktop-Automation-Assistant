import pyautogui
import time
import pygetwindow as gw
import webbrowser

# -------------------------------
#  KEYWORD GROUPS
# -------------------------------

PAUSE_KEYWORDS = [
    "pause", "pause it", "stop", "stop it", 
    "pause the music", "pause song", "stop music", 
    "pause video", "stop the song", "hold on", 
    "mute", "mute it", "shut up"
]

PLAY_KEYWORDS = [
    "resume", "play", "continue", "play it", "start playing"
]

REWIND_KEYWORDS = [
    "rewind", "go back", "back 10 seconds", 
    "back little", "rewind a bit"
]

FORWARD_KEYWORDS = [
    "forward", "skip", "ahead", "jump", 
    "go forward", "forward 10 seconds"
]

VOLUME_UP_KEYWORDS = [
    "volume up", "increase volume", "louder", 
    "sound up", "increase sound"
]

VOLUME_DOWN_KEYWORDS = [
    "volume down", "decrease volume", "lower volume", 
    "quiet", "reduce sound"
]

NEXT_VIDEO_KEYWORDS = [
    "next video", "skip video", "play next", "next", "play next video", "play next song"
]

PREVIOUS_VIDEO_KEYWORDS = [
    "previous video", "last video", "go back video", "previous"
]

FULLSCREEN_KEYWORDS = [
    "fullscreen", "full screen", "maximize video"
]

EXIT_FULLSCREEN_KEYWORDS = [
    "exit full screen", "minimize video", "small screen"
]

CLOSE_TAB_KEYWORDS = [
    "close tab", "close this", "close it", 
    "exit tab", "close youtube", "stop youtube", "close the song"
]


# -------------------------------
#  CONTROL FUNCTIONS
# -------------------------------

def pause_video():
    """Pauses or plays the YouTube video."""
    time.sleep(0.2)
    pyautogui.press("k")


def play_video():
    """Resumes or plays the video (same as pause toggle)."""
    time.sleep(0.2)
    pyautogui.press("k")


def rewind_video():
    """Rewinds 10 seconds."""
    time.sleep(0.2)
    pyautogui.press("j")


def forward_video():
    """Skips forward 10 seconds."""
    time.sleep(0.2)
    pyautogui.press("l")


def volume_up():
    """Increases the volume."""
    time.sleep(0.2)
    pyautogui.press("up")


def volume_down():
    """Decreases the volume."""
    time.sleep(0.2)
    pyautogui.press("down")


def next_video():
    """Plays the next video."""
    time.sleep(0.2)
    pyautogui.hotkey("shift", "n")


def previous_video():
    """Plays the previous video."""
    time.sleep(0.2)
    pyautogui.hotkey("shift", "p")


def fullscreen():
    """Enters fullscreen mode."""
    time.sleep(0.2)
    pyautogui.press("f")


def exit_fullscreen():
    """Exits fullscreen mode."""
    time.sleep(0.2)
    pyautogui.press("f")  # same key toggles fullscreen


def close_tab():
    """Closes the current browser tab."""
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "w")


def activate_chrome():
    """Safer Chrome activation without Windows 288 error."""
    windows = gw.getAllTitles()

    for w in windows:
        if "chrome" in w.lower():
            try:
                win = gw.getWindowsWithTitle(w)[0]

                # Restore if minimized
                try:
                    win.restore()
                except:
                    pass

                time.sleep(0.2)

                # Try to activate (Windows sometimes blocks it)
                try:
                    win.activate()
                except:
                    pass

                time.sleep(0.3)

                # Maximize if needed
                try:
                    win.maximize()
                except:
                    pass

                time.sleep(0.3)
                return True

            except Exception as e:
                print("Chrome activation error:", e)
                return False

    return False

def switch_to_youtube_tab():
    """Switch Chrome to a YouTube tab using tab search."""
    chrome_windows = gw.getWindowsWithTitle("Chrome")
    if not chrome_windows:
        return False

    win = chrome_windows[0]
    win.activate()
    time.sleep(0.2)

    # Open Chrome tab search
    pyautogui.hotkey("ctrl", "shift", "a")
    time.sleep(0.5)

    # Filter for YouTube tabs
    pyautogui.typewrite("youtube", interval=0.05)
    time.sleep(0.4)

    pyautogui.press("enter")
    time.sleep(1)

    return True


def play_song_in_same_tab(song):
    """Search and play a song on YouTube in the same tab."""

    url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"

    # STEP 1 — Make sure Chrome is active
    if not activate_chrome():
        # Chrome not open → open YouTube once
        webbrowser.open("https://www.youtube.com")
        time.sleep(3)
        activate_chrome()

    time.sleep(0.5)

    # STEP 2 — Try switching to YouTube tab
    youtube_open = switch_to_youtube_tab()

    # STEP 3 — Load the new search URL in SAME tab
    pyautogui.hotkey("ctrl", "l")   # focus URL bar
    time.sleep(0.3)
    pyautogui.typewrite(url, interval=0.02)
    pyautogui.press("enter")

    # STEP 4 — Wait for YouTube to load
    time.sleep(2.8)

    # STEP 5 — Click the page to ensure it's focused
    pyautogui.click(600, 350)   # click center of screen
    time.sleep(0.3)

    # STEP 6 — Move to first video result
    pyautogui.press("tab")
    time.sleep(0.2)

    # STEP 7 — Play first video
    pyautogui.press("enter")
