# 🎙️ VoxDesk

A powerful voice-controlled desktop assistant for Windows that lets you operate your PC using natural voice commands.

## ✨ Features

- **Voice Activation** – Wake the assistant with customizable trigger words
- **YouTube Control** – Play, pause, skip, rewind, and search videos hands-free
- **Chrome Automation** – Open tabs, search the web, and control volume
- **WhatsApp Desktop** – Send messages, search contacts, and navigate chats
- **App Launcher** – Open any application with a simple voice command
- **AI Fallback** – Intelligent responses for unrecognized commands
- **Auto Sleep** – Conserves resources by deactivating after idle timeout

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Windows OS
- Microphone

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/VoxDesk.git
cd VoxDesk

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

Say one of the wake words to activate, then speak your command!

## 📁 Project Structure

```
VoxDesk/
├── main.py                    # Main entry point and command loop
├── listener.py                # Speech recognition module
├── speech_engine.py           # Text-to-speech output
├── commands.py                # Command router and handler
├── ai_fallback.py             # AI-powered fallback responses
├── basic_controls.py          # System and app controls
├── youtube_controls.py        # YouTube playback automation
├── chrome_controls.py         # Browser control functions
├── whatsapp_desktop_controls.py # WhatsApp Desktop automation
├── focus_target.py            # Window focus management
├── get_focused_name.ahk       # AutoHotkey helper script
└── requirements.txt           # Python dependencies
```

## 🎤 Voice Commands

| Category | Example Commands |
|----------|------------------|
| **YouTube** | "play [song name]", "pause", "next video", "rewind" |
| **Browser** | "open new tab", "search for [query]", "volume up" |
| **WhatsApp** | "open WhatsApp", "send message to [contact]" |
| **System** | "open [app name]", "sleep", "exit" |

## 🛠️ Technologies

- **Speech Recognition** – Real-time voice input processing
- **pyttsx3 / pywhatkit** – Text-to-speech and automation
- **PyAutoGUI** – GUI automation for desktop control
- **AutoHotkey** – Window management integration

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ for hands-free productivity
</p>
