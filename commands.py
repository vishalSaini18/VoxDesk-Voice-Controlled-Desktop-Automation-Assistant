import webbrowser
import pywhatkit
import sys
from datetime import datetime
import re
from speech_engine import speak
from youtube_controls import (
    PAUSE_KEYWORDS, PLAY_KEYWORDS, REWIND_KEYWORDS, FORWARD_KEYWORDS,
    VOLUME_UP_KEYWORDS, VOLUME_DOWN_KEYWORDS, NEXT_VIDEO_KEYWORDS,
    PREVIOUS_VIDEO_KEYWORDS, FULLSCREEN_KEYWORDS, EXIT_FULLSCREEN_KEYWORDS,
    CLOSE_TAB_KEYWORDS,
    pause_video, play_video, rewind_video, forward_video,
    volume_up, volume_down, next_video, previous_video,
    fullscreen, exit_fullscreen, close_tab, play_song_in_same_tab
)



def respond(command):

    # Greetings
    if re.search(r"\bhi\b", command) or re.search(r"\bhello\b", command):
        speak("Hello! How can I help you today?")

    # Time
    elif "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    # Open sites
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    # Search on Google
    elif "search for" in command:
        query = command.split("search for")[-1].strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # Play Music on YouTube
    # elif command.startswith("play "):
    #     song = command.replace("play", "").replace("on youtube", "").strip()
    #     speak(f"Playing {song} on YouTube")
    #     pywhatkit.playonyt(song)

    elif command.startswith("play "):
        song = command.replace("play", "").replace("on youtube", "").strip()
        speak(f"Playing {song}")

        # If YouTube tab is already open → play in same tab
        play_song_in_same_tab(song)

    # ============================
    #    YOUTUBE CONTROLS
    # ============================

    # Pause / Stop
    elif any(word in command for word in PAUSE_KEYWORDS):
        speak("Pausing the video")
        pause_video()

    # Resume / Play
    elif any(word in command for word in PLAY_KEYWORDS):
        speak("Playing the video")
        play_video()

    # Rewind 10 seconds
    elif any(word in command for word in REWIND_KEYWORDS):
        speak("Rewinding")
        rewind_video()

    # Forward 10 seconds
    elif any(word in command for word in FORWARD_KEYWORDS):
        speak("Skipping ahead")
        forward_video()

    # Volume Up
    elif any(word in command for word in VOLUME_UP_KEYWORDS):
        speak("Turning volume up")
        volume_up()

    # Volume Down
    elif any(word in command for word in VOLUME_DOWN_KEYWORDS):
        speak("Turning volume down")
        volume_down()

    # Next Video
    elif any(word in command for word in NEXT_VIDEO_KEYWORDS):
        speak("Playing next video")
        next_video()

    # Previous Video
    elif any(word in command for word in PREVIOUS_VIDEO_KEYWORDS):
        speak("Going back to previous video")
        previous_video()

    # Fullscreen
    elif any(word in command for word in FULLSCREEN_KEYWORDS):
        speak("Going fullscreen")
        fullscreen()

    # Exit fullscreen
    elif any(word in command for word in EXIT_FULLSCREEN_KEYWORDS):
        speak("Exiting fullscreen")
        exit_fullscreen()

    # Close current tab
    elif any(word in command for word in CLOSE_TAB_KEYWORDS):
        speak("Closing the tab")
        close_tab()

    # Exit assistant
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        sys.exit()

    else:
        speak("I'm not sure how to help with that.")
