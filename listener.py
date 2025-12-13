import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.2
    r.non_speaking_duration = 0.5

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5)  # no phrase limit
        except sr.WaitTimeoutError:
            return None

    try:
        text = r.recognize_google(audio).lower()
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None
