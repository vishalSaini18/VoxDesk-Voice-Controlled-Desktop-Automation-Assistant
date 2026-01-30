import pyautogui
import time
import pygetwindow as gw
import win32process
import win32gui
import psutil

Opening_WHATSAPP_KEYWORDS = [
    "open whatsapp", "activate whatsapp", "launch whatsapp", "start whatsapp", "whatsapp opne kr", "whatsapp kholo",
    "whatsapp khol", "whatsapp khol de", "whatsapp on kr", "whatsapp chalu kr", "whatsapp chalu kar de"]

GO_BACK_TO_CHATS_KEYWORDS = [
    "go to chats",
    "go to chat",
    "back",
    "chats",
    "back to chats",
    "open chats",
    "open chat"
    "close chat",
    "exit chat",
    "return to chats",
    "previous",
    "cancel",
    "go back to chats",
    "chats kholo",
    "chat kholo",
    "chat khol",
    "chats khol",
    "go back to chats",
    "go back to chat"
]

UNREAD_MESSAGE_KEYWORDS = [
    "check messages",
    "check unread",
    "open unread",
    "unread messages",
    "show unread",
    "go to unread",
    "go to messages",
    "go to unread messages",
    "go to unread chats"
]

Close_WHATSAPP_KEYWORDS = [
    "close whatsapp", "exit whatsapp", "quit whatsapp", "shutdown whatsapp", "whatsapp band kr", "whatsapp band kar de"]

def activate_whatsapp_desktop():
    # 1️⃣ If WhatsApp Desktop already open → activate ONLY exact title
    for win in gw.getWindowsWithTitle("WhatsApp"):
        if win.title.strip() == "WhatsApp":   # 🔥 EXACT MATCH
            try:
                if win.isMinimized:
                    win.restore()
                win.activate()
                time.sleep(0.4)
                return True
            except:
                pass

    # 2️⃣ Open Windows search (only if exact window not found)
    pyautogui.hotkey("win")
    time.sleep(0.6)

    # 3️⃣ Type WhatsApp and launch
    pyautogui.typewrite("whatsapp", interval=0.05)
    time.sleep(0.8)
    pyautogui.press("enter")

def search_contact(name):
    
    time.sleep(0.2)

    # Ctrl + F focuses search in WhatsApp Desktop
    pyautogui.hotkey("ctrl", "f")
    pyautogui.hotkey("ctrl", "a")

    time.sleep(0.3)

    pyautogui.typewrite(name, interval=0.05)
    time.sleep(1)

    # Open first result
    pyautogui.press("enter")

def send_message_to_contact(name):
    activate_whatsapp_desktop()
    time.sleep(0.2)
    search_contact(name)

def type_message_whatsapp(message):
    """
    Opens first contact if search is active
    and types the message in chat input
    """

    # Open first contact (safe even if chat already open)
    pyautogui.press("enter")
    time.sleep(0.4)

    if not message:
        return

    # Type message
    pyautogui.typewrite(message, interval=0.03)

def clear_message_whatsapp():
    """
    Clears the current typed message in WhatsApp chat input
    """

    # Select all text in message box
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)

    # Delete it
    pyautogui.press("backspace")

def send_message(message):
    pyautogui.typewrite(message, interval=0.03)
    pyautogui.press("enter")

def go_back_to_chats():
    """
    Forces WhatsApp focus and returns to chat list
    Works from chat, search, typing box, or idle state
    """

    # # Clear any current focus
    # pyautogui.press("esc")
    # time.sleep(0.1)

    # # Tab through UI to reach search bar
    # for _ in range(4):
    #     pyautogui.press("tab")
    #     time.sleep(0.08)

    pyautogui.hotkey("ctrl", "alt", "/")

    # Esc to exit search and return to chat list
    pyautogui.press("esc")
    time.sleep(0.1)
    go_to_unread_messages()

def go_to_unread_messages():
    pyautogui.hotkey("tab")
    time.sleep(0.3)
    pyautogui.hotkey("ctrl","alt","/")

    # Tab through UI to reach search bar
    for _ in range(2):
        pyautogui.press("tab")
        time.sleep(0.08)

def next_chat():
    """
    Opens the next chat in WhatsApp Desktop
    Assumes WhatsApp is already active
    """

    pyautogui.hotkey("down")
    time.sleep(0.3)
    pyautogui.press("enter")

def close_whatsapp():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == "whatsapp.exe":
            proc.kill()
            return True
    return False