from speech_engine import speak
from listener import listen
from commands import respond

speak("Bitch activated.")

while True:
    command = listen()

    print(f"Command received: {command}")

    if command:
        respond(command)
    else:
        print("No valid command detected.")
