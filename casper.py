import os
import time
import subprocess
import webbrowser

import speech_recognition as sr
import pyttsx3
import pyautogui

APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "vs code": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
}


# 1. TEXT-TO-SPEECH ENGINE

def speak(text: str):
    print(f"Casper: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)
        
        voices = engine.getProperty("voices")
        for voice in voices:
            name = voice.name.lower()
            if "david" in name or "male" in name or "mark" in name or "george" in name:
                engine.setProperty("voice", voice.id)
                break
                
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Voice Error]: {e}")


# 2. SPEECH RECOGNITION (Listening for commands)
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8

def listen(timeout=5, phrase_time_limit=6) -> str:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.4)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return ""
    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("I can't reach the internet right now.")
        return ""


# 
# 3. HELPER FUNCTIONS
# 
def open_application(app_key: str) -> bool:
    """Launches local application from APP_PATHS"""
    path = APP_PATHS.get(app_key)
    if not path:
        return False
    path = os.path.expandvars(path)
    try:
        subprocess.Popen(path)
        return True
    except Exception:
        return False

def open_in_chrome(url: str):
    """Forces the browser link to open in Google Chrome for logged-in sessions"""
    chrome_path = os.path.expandvars(APP_PATHS["chrome"])
    if os.path.exists(chrome_path):
        subprocess.Popen([chrome_path, url])
    else:
        # Fallback to default browser if chrome path is wrong
        webbrowser.open(url)


# 4. SMART COMMAND HANDLER
def handle_command(command: str):
    if not command:
        speak("I didn't catch that.")
        return

    if any(word in command for word in ["exit", "quit", "shut down", "stop"]):
        speak("Okay Mam Taibah, going offline. Call me anytime.")
        raise SystemExit

    # --- 1. File Explorer / Folders ---
    elif "file explorer" in command or "files" in command or "folder" in command:
        os.startfile(os.path.expanduser("~"))
        speak("Opening File Explorer.")
        return

    # --- 2. Live Dictation Mode (Works in VS Code, Notepad, Word etc.) ---
    elif "start dictation" in command or "dictate" in command or "start typing" in command:
        speak("Dictation mode activated. Speak now. Say 'stop dictation' to finish.")
        time.sleep(1.0)
        while True:
            text = listen(timeout=5, phrase_time_limit=8)
            if "stop dictation" in text or "stop writing" in text or "stop typing" in text:
                speak("Dictation stopped.")
                break
            if text:
                # Types live in active window
                pyautogui.typewrite(text + " ", interval=0.01)
        return

    # --- 3. Single Line Type Command ---
    elif "type" in command or "write" in command:
        text_to_type = command.replace("type", "").replace("write", "").strip()
        if text_to_type:
            speak(f"Typing: {text_to_type}")
            time.sleep(1.0)
            pyautogui.typewrite(text_to_type + " ", interval=0.01)
        else:
            speak("What should I type?")
        return

    # --- 4. YouTube Video Play & Search ---
    elif "play" in command or "youtube" in command:
        query = command.replace("play", "").replace("on youtube", "").replace("youtube", "").replace("search", "").strip()
        if query:
            speak(f"Searching for {query} on YouTube in Google Chrome.")
            yt_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            open_in_chrome(yt_url)
        else:
            speak("What should I play on YouTube?")
        return

    # --- 5. Open Websites & Apps in Chrome ---
    elif "open" in command:
        target = command.replace("open", "").strip()
        
        known_sites = {
            "youtube": "https://www.youtube.com",
            "gmail": "https://mail.google.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "insta": "https://www.instagram.com",     
            "instaa": "https://www.instagram.com",    
            "google": "https://www.google.com",
        }
        
        # Open in Chrome
        if target in known_sites:
            open_in_chrome(known_sites[target])
            speak(f"Opening {target} in Chrome.")
            return
            
        # Open local app (like VS Code, Notepad, Excel)
        for app_key in APP_PATHS:
            if app_key in target:
                if open_application(app_key):
                    speak(f"Opening {app_key}.")
                    return
                    
        # Fallback website or Google Search
        if "." in target or "website" in target:
            url = f"https://www.{target}" if not target.startswith("http") else target
            open_in_chrome(url)
            speak(f"Opening {target} in Chrome.")
        else:
            speak(f"Searching Google for {target}.")
            search_url = f"https://www.google.com/search?q={target.replace(' ', '+')}"
            open_in_chrome(search_url)
        return

    else:
        speak("Sorry, I don't have that command yet.")


# ----------------------------------------------------------------------
# 5. MAIN LOOP (Only Voice-Activated)
# ----------------------------------------------------------------------
def main():
    speak("Casper is now online.")
    while True:
        print("\nListening for the wake word 'Casper'...")
        heard = listen(timeout=3, phrase_time_limit=4)
        
        if "casper" in heard:
            speak("Mam Taibah, I am Casper. How can I help you?")
            command = listen(timeout=6, phrase_time_limit=8)
            try: 
                handle_command(command)
            except SystemExit: 
                break
            time.sleep(1.5)


if __name__ == "__main__":
    main()