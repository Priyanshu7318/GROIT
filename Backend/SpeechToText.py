"""
Lightweight SpeechToText stub.

The original implementation used Selenium, Chrome, and a generated Voice.html
page to capture microphone input. That code is intentionally removed.

Jarvis now relies on text input (web UI via api_bridge.py / UserInput.data
or terminal input) for all interactions. This module only exposes a
SpeechRecognition() function so that Main.py can import it without errors.
"""

def SpeechRecognition():
    return ""

