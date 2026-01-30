import pyttsx3
import threading

stop_flag = False
is_speaking = False
current_engine = None

lock = threading.Lock()
engine_lock = threading.Lock()


def speak(text, speed=160):
    global stop_flag, is_speaking, current_engine

    with lock:
        stop_flag = False
        is_speaking = True

    def run():
        global stop_flag, is_speaking, current_engine

        with engine_lock:
            engine = pyttsx3.init()
            current_engine = engine

            try:
                engine.setProperty("rate", speed)

                for v in engine.getProperty("voices"):
                    if "zira" in v.id.lower():
                        engine.setProperty("voice", v.id)
                        break

                engine.say(text)
                engine.runAndWait()

            finally:
                try:
                    engine.stop()
                except:
                    pass

                current_engine = None
                is_speaking = False

    threading.Thread(target=run, daemon=True).start()


def stop_speak():
    global stop_flag, current_engine

    with lock:
        stop_flag = True

    # 🔥 THIS IS THE REAL STOP
    if current_engine:
        try:
            current_engine.stop()
        except:
            pass        