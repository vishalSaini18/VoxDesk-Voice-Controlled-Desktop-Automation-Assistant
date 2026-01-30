import webbrowser
import pywhatkit
import sys
from datetime import datetime
import re
from speech_engine import speak, stop_speak, is_speaking    
from ai_fallback import ai_reply
import time
import os
import pyautogui
from focus_target import (FOCUS_PREFIXES, OPEN_PREFIXES, 
    focus_window, focus_target, open_target, stop_focus_search)

from basic_controls import (
    TIME_KEYWORDS, OPEN_GOOGLE_KEYWORDS, OPEN_YOUTUBE_KEYWORDS,
    focus_search_PREFIX, GOOGLE_SEARCH_PREFIX, SHUTDOWN_KEYWORDS,
    restore_window_keywords,maximize_window_keywords,CLOSE_TAB_KEYWORDS,press_button_prefix,
    Typing_prefix, go_forward_keywords, close_active_window_keywords,BRIGHTNESS_UP_KEYWORDS, BRIGHTNESS_DOWN_KEYWORDS,
    scroll_up_keywords, scroll_down_keywords, left_click_keywords, right_click_keywords,lock_screen_keywords,
    go_to_desktop_keywords,

    go_back, go_forward, tell_time, open_google, open_youtube, focus_search, google_search, shutdown_pc,
    maximize_window, restore_window, next_tab, previous_tab, close_tab, press_button,
    type_basic, close_active_window, brightness_up, brightness_down,
    scroll_up, scroll_down, left_click, right_click,lock_screen,go_to_desktop
)

from youtube_controls import (
    PAUSE_KEYWORDS, PLAY_KEYWORDS, REWIND_KEYWORDS, FORWARD_KEYWORDS, NEXT_VIDEO_KEYWORDS,
    PREVIOUS_VIDEO_KEYWORDS, PLAY_SONG_PREFIX,
    
    play_song_command,
    pause_video, play_video, rewind_video, forward_video,
    next_video, previous_video,
    play_song_in_same_tab, activate_chrome
)

from chrome_controls import (
    VOLUME_UP_KEYWORDS, VOLUME_DOWN_KEYWORDS, open_new_tab_keywords, search_in_browser_prefix,
    activate_chrome_keywords,

    volume_up, volume_down,
    activate_chrome_cmd,
    open_new_tab,
    search_in_browser
)


from whatsapp_desktop_controls import (
    Opening_WHATSAPP_KEYWORDS,
    GO_BACK_TO_CHATS_KEYWORDS,
    UNREAD_MESSAGE_KEYWORDS,
    send_message_to_contact,
    Close_WHATSAPP_KEYWORDS,

    activate_whatsapp_desktop,
    search_contact,
    send_message,
    go_back_to_chats,
    type_message_whatsapp,
    clear_message_whatsapp,
    go_to_unread_messages,
    next_chat,
    close_whatsapp
)


def respond(command):

    # ============================
    #    BASIC COMMANDS
    # ============================

    # Time
    if command in TIME_KEYWORDS:
        tell_time(speak)

    elif command in ["stop", "quiet", "shut up", "chup", "bas"]:
        stop_speak()
        stop_focus_search()  # Also stop any ongoing focus/open search
        return

    # Go to Desktop (minimize all windows)
    elif command in go_to_desktop_keywords:
        go_to_desktop()

    elif command in OPEN_GOOGLE_KEYWORDS:
        open_google(speak)

    # Open YouTube
    elif command in OPEN_YOUTUBE_KEYWORDS:
        open_youtube(speak)

    # uses Ctrl+F (works in WhatsApp Desktop, browsers, VS Code, etc.)
    elif any(command.startswith(p) for p in focus_search_PREFIX):
        focus_search(command, speak)

    # Google Search
    elif any(command.startswith(p) for p in GOOGLE_SEARCH_PREFIX):
        google_search(command, speak)
    
    # Go back
    elif command in ["go back", "previous page"]:
        speak("Going back")
        go_back()

    # Go forward
    elif command in go_forward_keywords :
        speak("Going forward")
        go_forward()

    # Fullscreen
    elif command in maximize_window_keywords :
        speak("Going fullscreen")
        maximize_window()

    # Exit fullscreen
    elif command in restore_window_keywords :
        speak("Exiting fullscreen")
        restore_window()

    # Shutdown PC
    elif command in SHUTDOWN_KEYWORDS:
        shutdown_pc(speak)

    # ---------- PRESS BUTTON ----------
    elif any(command.startswith(p) for p in press_button_prefix):
        button = command
        for p in press_button_prefix:
            button = button.replace(p, "").strip()
        if button:
            press_button(button)
        else:
            speak("Please specify a button to press.")

    # ---------- TYPE BASIC ----------
    elif any(command.startswith(p) for p in Typing_prefix):
        message = command
        for p in Typing_prefix:
            message = message.replace(p, "").strip()
        if message:
            type_basic(message)
        else:
            speak("Please specify a message to type.")

    # Close active window
    elif command in close_active_window_keywords:
        speak("Closing the active window")
        close_active_window()

    # ---------- STARTS WITH "BRIGHTNESS" ----------
    elif (any(command.startswith(k) for k in BRIGHTNESS_UP_KEYWORDS)):
        match = re.search(r"by (\d+)", command)
        step = int(match.group(1)) if match else 10
        brightness_up(step)

    elif any(command.startswith(k) for k in BRIGHTNESS_DOWN_KEYWORDS):
        match = re.search(r"by (\d+)", command)
        step = int(match.group(1)) if match else 10
        brightness_down(step)

    # ---------- SCROLLING ----------
    elif command in scroll_up_keywords:
        scroll_up()
     
    elif command in scroll_down_keywords:
        scroll_down()

    elif command in left_click_keywords:    
        left_click()
    
    elif command in right_click_keywords:
        right_click()

    elif command in lock_screen_keywords:
        speak("Locking the screen")
        lock_screen()
        
    # ============================
    #    YOUTUBE CONTROLS
    # ============================
    
    elif command.startswith(f"{PLAY_SONG_PREFIX} "):
        song = command.replace(f"{PLAY_SONG_PREFIX} ", "", 1).strip()
        play_song_in_same_tab(song)

    # Pause / Stop
    elif command in PAUSE_KEYWORDS:
        speak("Pausing the video")
        pause_video()

    # Resume / Play
    elif command in PLAY_KEYWORDS:
        speak("Playing the video")
        play_video()

    # Rewind 10 seconds
    elif command in REWIND_KEYWORDS :
        speak("Rewinding")
        rewind_video()

    # Forward 10 seconds
    elif command in FORWARD_KEYWORDS :
        speak("Skipping ahead")
        forward_video()

    # Next Video
    elif command in NEXT_VIDEO_KEYWORDS :
        speak("Playing next video")
        next_video()

    # Previous Video
    elif command in PREVIOUS_VIDEO_KEYWORDS :
        speak("Going back to previous video")
        previous_video()
    
    # Exit assistant
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        sys.exit()

    # ============================
    #    CHROME COMMANDS
    # ============================

    # ---------- STARTS WITH "VOLUME" ----------
    elif command.startswith("volume"):

        # volume up
        if "up" in command:
            match = re.search(r"by (\d+)", command)
            if match:
                volume_up(int(match.group(1)))
            else:
                volume_up(command.count("up") or 1)

        # volume down
        elif "down" in command:
            match = re.search(r"by (\d+)", command)
            if match:
                volume_down(int(match.group(1)))
            else:
                volume_down(command.count("down") or 1)


    # ---------- DOES NOT START WITH "VOLUME" ----------
    # volume up keywords
    elif any(command.startswith(k) for k in VOLUME_UP_KEYWORDS):
        match = re.search(r"by (\d+)", command)
        volume_up(int(match.group(1)) if match else 1)

    # volume down keywords
    elif any(command.startswith(k) for k in VOLUME_DOWN_KEYWORDS):
        match = re.search(r"by (\d+)", command)
        volume_down(int(match.group(1)) if match else 1)

    # Close current tab
    elif command in CLOSE_TAB_KEYWORDS:
        speak("Closing the tab")
        close_tab()
    
    # Move to next Chrome tab
    elif any(phrase in command for phrase in [
        "next tab",
        "move to next tab",
        "switch to next tab",
        "go to next tab"
    ]):
        if next_tab():
            speak("Next tab")
        else:
            speak("Chrome is not active")

    # Move to previous Chrome tab
    elif any(phrase in command for phrase in [
        "previous tab",
        "move to previous tab",
        "switch to previous tab",
        "go to previous tab",
        "last tab"
    ]):
        if previous_tab():
            speak("Previous tab")
        else:
            speak("Chrome is not active")

    # Activate Chrome
    elif command in activate_chrome_keywords:
        if activate_chrome():
            speak("Chrome activated")
        else:
            speak("Chrome is not running")

    elif command in open_new_tab_keywords:
        open_new_tab()

    elif any(command.startswith(p) for p in search_in_browser_prefix):
        search_in_browser(command)

    # ============================
    #    WHATSAPP DESKTOP COMMANDS
    # ============================

    elif any(word in command for word in Opening_WHATSAPP_KEYWORDS):
        speak("Opening WhatsApp")
        activate_whatsapp_desktop()

    elif command.startswith("search whatsapp"):
        # example: search whatsapp rahul
        name = command.replace("search whatsapp", "").strip()
        speak(f"Searching {name} on WhatsApp")
        search_contact(name)

    elif command == "select contact" or command == "open chat" or command == "go to chat" or command == "open":
        pyautogui.press("enter")

    elif command.startswith("send message to"):
        name = command.replace("send message to", "").strip()
        speak(f"Sending message to {name}")
        send_message_to_contact(name)

    elif command.startswith("type message"):
        message = command.replace("type message", "").strip()

        if message:
            speak("Typing")
            type_message_whatsapp(message)

    elif command in ["clear message", "delete message", "remove message", "clear all", "clear the message"]:
        speak("Clearing message")
        clear_message_whatsapp()

    elif command in GO_BACK_TO_CHATS_KEYWORDS:
        go_back_to_chats()

    elif command == "next chat" or command == "next message":
        next_chat()

    elif command in UNREAD_MESSAGE_KEYWORDS:
        go_to_unread_messages()

    elif command == "send message":
        pyautogui.press("enter")

    elif command in Close_WHATSAPP_KEYWORDS:
        if not close_whatsapp():
            speak("WhatsApp is not running")

    # ---------- FOCUS TARGET (scan desktop/zones with TAB + arrow keys) ----------
    elif any(command.startswith(p) for p in FOCUS_PREFIXES):
        target = command
        for p in FOCUS_PREFIXES:
            if target.startswith(p):
                target = target.replace(p, "", 1).strip()
                break

        if target:
            speak(f"Focusing {target}")
            if not focus_target(target):
                speak(f"{target} not found")
        return

    # ---------- OPEN TARGET (find and open file/app) ----------
    elif any(command.startswith(p) for p in OPEN_PREFIXES):
        target = command
        for p in OPEN_PREFIXES:
            if target.startswith(p):
                target = target.replace(p, "", 1).strip()
                break

        if target:
            speak(f"Focusing {target}")
            if not open_target(target):
                speak(f"{target} not found")
        return


    # ============================
    #    AI FALLBACK
    # ============================

    else:
        reply = ai_reply(command)

        if reply:
            print("AI:", reply)
            speak(reply)
        else:
            print("AI: No response")
            speak("I don't have an answer for that.")


