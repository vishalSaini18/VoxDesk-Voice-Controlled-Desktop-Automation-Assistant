import speech_recognition as sr
import queue

# def listen():
#     r = sr.Recognizer()
#     r.dynamic_energy_threshold = True
#     r.pause_threshold = 0.8
#     r.non_speaking_duration = 0.5

#     with sr.Microphone() as source:
#         print("Listening...")
#         r.adjust_for_ambient_noise(source, duration=0.5)
#         try:
#             audio = r.listen(source, timeout=5)  # no phrase limit
#         except sr.WaitTimeoutError:
#             return None

#     try:
#         text = r.recognize_google(audio).lower()
#         return text
#     except sr.UnknownValueError:
#         return None
#     except sr.RequestError:
#         return None



# 1️⃣ Create recognizer FIRST
recognizer = sr.Recognizer()

# 2️⃣ THEN set tuning parameters
recognizer.pause_threshold = 1.0
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.6

# 3️⃣ Mic + queue
mic = sr.Microphone()
audio_queue = queue.Queue()

def callback(recognizer, audio):
    audio_queue.put(audio)

# 4️⃣ Calibrate once
with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.5)

# 5️⃣ Background listener (keeps mic open)
stopper = recognizer.listen_in_background(mic, callback)

def listen():
    try:
        audio = audio_queue.get(timeout=0.1)
    except queue.Empty:
        return None

    try:
        return recognizer.recognize_google(audio).lower()
    except:
        return None