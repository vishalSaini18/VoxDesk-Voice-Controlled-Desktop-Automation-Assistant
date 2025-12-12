import pyttsx3

def speak(text, speed=160):
    engine = pyttsx3.init()

    # Set Indian female voice if installed
    voices = engine.getProperty('voices')
    selected = False
    for v in voices:
        if "en-in" in v.id.lower() or "neerja" in v.id.lower():
            engine.setProperty('voice', v.id)
            selected = True
            break

    # If Indian voice not found, fallback to any female voice
    if not selected:
        for v in voices:
            if "female" in v.id.lower() or "zira" in v.id.lower():
                engine.setProperty('voice', v.id)
                break

    engine.setProperty('rate', speed)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
