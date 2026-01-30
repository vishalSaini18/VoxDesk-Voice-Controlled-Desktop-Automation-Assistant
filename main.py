from speech_engine import speak, stop_speak, is_speaking
from listener import listen
from commands import respond
import time

speak("Bitch activated.")

WAKE_WORDS = [
    "bitch activate", "hey bitch", "bitch", "fucking bitch", "alexa",
    "jarvis", "hey jarvis", "jorvis", "hey jorvis", "siri","hey siri", "kutte", "uth ja kutte"
]

SLEEP_WORDS = ["sleep", "deactivate", "quiet", "chup kar kutte", "chup", "chup karbe kutte", "chup kar be kutte"]

INTERRUPT_WORDS = [
    "shut up", "stop", "quiet", "bas", "chup"
]

ACTIVE_TIMEOUT = 600
  # seconds

active = True                    # active initially
last_active_time = time.time()   # start timer

while True:
    command = listen()

    # 🔹 Ignore empty polls
    if command is None:
        if active and time.time() - last_active_time > ACTIVE_TIMEOUT:
            active = False
            speak("Deactivated.")
        time.sleep(0.05)
        continue

    command = command.lower()
    print(f"Command received: {command}")

    # 🔥 GLOBAL INTERRUPT (works even while speaking)
    if is_speaking and any(w in command for w in INTERRUPT_WORDS):
        stop_speak()
        continue

    # Exit command
    if command == "exit":
        stop_speak()
        speak("Goodbye.")
        break

    # Wake words (when inactive)
    if not active:
        if any(w in command for w in WAKE_WORDS):
            active = True
            last_active_time = time.time()
            speak("Bitch activated.")
        continue

    # Reset active timer
    last_active_time = time.time()

    # Manual sleep
    if command in SLEEP_WORDS:
        active = False
        speak("Deactivated.")
        continue

    # Normal command execution
    respond(command)
    

# while True:
#     command = input(">> ").strip().lower()

#     if not command:
#         continue

#     print(f"Command received: {command}")

#     # Exit program
#     if command == "exit":
#         speak("Goodbye.")
#         break

#     # Wake word detection (when inactive)
#     if not active:
#         if any(w in command for w in WAKE_WORDS):
#             active = True
#             last_active_time = time.time()
#             speak("Activated.")
#         continue

#     # Reset timer on any valid command while active
#     last_active_time = time.time()

#     # Manual sleep
#     if command in SLEEP_WORDS:
#         active = False
#         speak("Deactivated.")
#         continue

#     # Execute command
#     respond(command)


