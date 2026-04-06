import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Backend Imports
try:
    from Backend.Model import FirstLayerDMM
except Exception as e:
    print("Failed to import Backend.Model:", e)
    raise

try:
    from Backend.RealtimeSearchEngine import RealtimeSearchEngine
except Exception as e:
    print("Failed to import Backend.RealtimeSearchEngine:", e)
    def RealtimeSearchEngine(q): return "Realtime search unavailable"

try:
    from Backend.Automation import Automation
except Exception as e:
    print("Failed to import Backend.Automation:", e)
    def Automation(args): return None

try:
    from Backend.SpeechToText import SpeechRecognition
except Exception as e:
    print("Failed to import Backend.SpeechToText:", e)
    def SpeechRecognition(): return input("You: ")

try:
    from Backend.Chatbot import ChatBot
except Exception as e:
    print("Failed to import Backend.Chatbot:", e)
    def ChatBot(q): return "Chatbot unavailable"

try:
    from Backend.TextToSpeech import TextToSpeech
except Exception as e:
    print("Failed to import Backend.TextToSpeech:", e)
    def TextToSpeech(text): pass

try:
    from Backend.Extraction import Extraction
except Exception as e:
    print("Failed to import Backend.Extraction:", e)
    def Extraction(): return "Extraction unavailable"

from dotenv import dotenv_values
from asyncio import run as asyncio_run
from time import sleep
import subprocess
import threading
import json
import os
import inspect

env_vars = dotenv_values(PROJECT_ROOT / ".env")
Username = env_vars.get("Username", "User")
AssistantName = env_vars.get("AssistantName", "Assistant")

DefaultMessage = f"{Username}: Hello {AssistantName}, How are you?\n{AssistantName}: Welcome {Username}, I am doing well. How may I help you?"

subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search", "reminder"]

DATA_DIR = PROJECT_ROOT / "Data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHATLOG_PATH = DATA_DIR / "ChatLog.json"
if not CHATLOG_PATH.exists():
    CHATLOG_PATH.write_text("[]", encoding="utf-8")

# --- Helper Functions (Previously imported from GUI) ---
def TempDirectoryPath(filename):
    path = PROJECT_ROOT / "Data" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)

def ShowTextToScreen(Text):
    path = Path(TempDirectoryPath("Responses.data"))
    path.write_text(Text, encoding="utf-8")
    # Also print to terminal for user visibility (especially if GUI is down)
    print(f"\n{Text}")

def SetAssistantStatus(status):
    path = Path(TempDirectoryPath("Status.data"))
    path.write_text(status, encoding="utf-8")

def GetAssistantStatus():
    path = Path(TempDirectoryPath("Status.data"))
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Available..."

def SetMicrophoneStatus(command):
    path = Path(TempDirectoryPath("Mic.data"))
    path.write_text(command, encoding="utf-8")

def GetMicrophoneStatus():
    path = Path(TempDirectoryPath("Mic.data"))
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "False"

import re

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    
    # Remove common meta-commentary
    patterns = [
        r"The search results for .*? are:",
        r"Based on the reference provided,.*",
        r"Based on the provided.*",
        r"I will use it to answer.*",
        r"\[start\]",
        r"\[end\]",
        r"So, the time right now is", # Clean time redundancy if needed, though my previous fix handles time better.
        r"It seems you haven't asked.*", # Don't strip this if it's the only answer, but good to clean prefixes
    ]
    
    for pattern in patterns:
        modified_answer = re.sub(pattern, "", modified_answer, flags=re.IGNORECASE).strip()
    
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split(' ')
    question_words = ["how", "what", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

# --- End Helpers ---

def ShowDefaultChatInNoChats():
    try:
        raw = CHATLOG_PATH.read_text(encoding="utf-8")
        if len(raw.strip()) <= 2:
            Path(TempDirectoryPath('Database.data')).write_text("", encoding='utf-8')
            Path(TempDirectoryPath('Responses.data')).write_text(DefaultMessage, encoding='utf-8')
    except Exception:
        Path(TempDirectoryPath('Database.data')).write_text("", encoding='utf-8')
        Path(TempDirectoryPath('Responses.data')).write_text(DefaultMessage, encoding='utf-8')

def ReadChatlogJson():
    try:
        return json.loads(CHATLOG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []

def ChatlogIntegration():
    json_data = ReadChatlogJson()
    formatted = ""
    for entry in json_data:
        role = str(entry.get("role", "")).lower()
        content = entry.get("content", "")
        if role == "user":
            formatted += f"{Username}: {content}\n"
        else:
            formatted += f"{AssistantName}: {content}\n"
    Path(TempDirectoryPath('Database.data')).write_text(AnswerModifier(formatted), encoding='utf-8')

def ShowChatsOnGUI():
    dbp = Path(TempDirectoryPath('Database.data'))
    resp = Path(TempDirectoryPath('Responses.data'))
    try:
        data = dbp.read_text(encoding='utf-8') if dbp.exists() else ""
        if data:
            resp.write_text(data, encoding='utf-8')
    except Exception:
        pass

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatInNoChats()
    ChatlogIntegration()
    ShowChatsOnGUI()

InitialExecution()

def _run_maybe_async(fn, *args, **kwargs):
    try:
        if inspect.iscoroutinefunction(fn):
            return asyncio_run(fn(*args, **kwargs))
        else:
            return fn(*args, **kwargs)
    except Exception as e:
        print("Error running function:", e)
        return None

Authenticated = False

def MainExecution():
    global Authenticated

    try:
        # Check for web-based authentication
        auth_file = PROJECT_ROOT / "Data" / "Auth.data"
        if auth_file.exists() and auth_file.read_text(encoding='utf-8').strip() == "True":
            Authenticated = True

        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""

        SetAssistantStatus("Listening...")
        
        # Define Path locally to ensure access
        UserInputPath = PROJECT_ROOT / "Data" / "UserInput.data"

        if UserInputPath.exists() and UserInputPath.stat().st_size > 0:
            Query = UserInputPath.read_text(encoding='utf-8').strip()
            UserInputPath.write_text("", encoding='utf-8')
        else:
            Query = ""
            
        if not Authenticated:
            if Query and "hello" in Query.lower():
                print("Authentication Required. Please enter password in terminal or log in via Web UI.")
                _run_maybe_async(TextToSpeech, "Please authenticate to proceed.")
                
                # Check for web auth again before asking terminal
                if auth_file.exists() and auth_file.read_text(encoding='utf-8').strip() == "True":
                    Authenticated = True
                else:
                    try:
                        # Set a timeout for input if possible, but standard input.input() is blocking.
                        # For now, we'll keep it simple but suggest web login.
                        print("Waiting for terminal password (or log in via Web UI)...")
                        Password = input("Enter Password: ")
                        if Password == "ansh@7318":
                            Authenticated = True
                            auth_file.write_text("True", encoding='utf-8')
                    except EOFError:
                        Password = ""
                
                if Authenticated:
                    print("Access Granted.")
                    _run_maybe_async(TextToSpeech, "Access Granted. Welcome back.")
                else:
                    print("Access Denied.")
                    _run_maybe_async(TextToSpeech, "Access Denied.")
                    return False
            else:
                if Query:
                    _run_maybe_async(TextToSpeech, "System Locked. Please log in.")
                return False

        if not Query:
            SetAssistantStatus("Available...")
            return False
            
        if not Query:
            SetAssistantStatus("Available...")
            return False

        ShowTextToScreen(f"{Username}: {Query}")
        SetAssistantStatus("Thinking...")

        # Extraction Feature
        if "extract info" in Query.lower():
            SetAssistantStatus("Extracting...")
            Answer = Extraction()
            ShowTextToScreen(f"{AssistantName} : {Answer}")
            SetAssistantStatus("Answering...")
            _run_maybe_async(TextToSpeech, "Here is the summary of your conversation.")
            return True

        Decision = FirstLayerDMM(Query) or ["general " + Query]
        print("Decision:", Decision)

        G = any(i.startswith("general") for i in Decision)
        R = any(i.startswith("realtime") for i in Decision)
        merged_query = " and ".join(
            [" ".join(i.split()[1:]).strip() for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )

        for q in Decision:
            if q.startswith("generate") or "generate image" in q:
                ImageGenerationQuery = q
                ImageExecution = True

        for q in Decision:
            if not TaskExecution and any(q.startswith(func) for func in Functions):
                try:
                    _run_maybe_async(Automation, Decision)
                except Exception as e:
                    print("Automation error:", e)
                TaskExecution = True

        if ImageExecution:
            (PROJECT_ROOT / "Data").mkdir(exist_ok=True, parents=True)
            (PROJECT_ROOT / "Data" / "ImageGeneration.data").write_text(f"{ImageGenerationQuery},True", encoding='utf-8')
            try:
                p1 = subprocess.Popen([sys.executable, str(PROJECT_ROOT / "Backend" / "ImageGeneration.py")],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocesses.append(p1)
            except Exception as e:
                print("Failed to start image generation:", e)

        if R and not TaskExecution:
            SetAssistantStatus("Searching...")
            Answer = _run_maybe_async(RealtimeSearchEngine, QueryModifier(merged_query))
            if Answer:
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering...")
                _run_maybe_async(TextToSpeech, Answer)
            return True

        for q in Decision:
            if q.startswith("general"):
                SetAssistantStatus("Thinking...")
                QueryFinal = q.replace("general", "").strip()
                Answer = _run_maybe_async(ChatBot, QueryModifier(QueryFinal))
                Answer = Answer or "Sorry, I couldn't generate an answer."
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering...")
                _run_maybe_async(TextToSpeech, Answer)
                return True

            if q.startswith("realtime"):
                SetAssistantStatus("Searching...")
                QueryFinal = q.replace("realtime", "").strip()
                Answer = _run_maybe_async(RealtimeSearchEngine, QueryModifier(QueryFinal))
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering...")
                _run_maybe_async(TextToSpeech, Answer)
                return True

            if q.strip() in ["exit", "quit", "close"]:
                Answer = _run_maybe_async(ChatBot, "Okay, Bye!")
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering...")
                _run_maybe_async(TextToSpeech, Answer)
                os._exit(0)

        SetAssistantStatus("Thinking...")
        Answer = _run_maybe_async(ChatBot, QueryModifier(merged_query or Query))
        if Answer:
            ShowTextToScreen(f"{AssistantName} : {Answer}")
            SetAssistantStatus("Answering...")
            _run_maybe_async(TextToSpeech, Answer)
        return True

    except Exception as e:
        print("MainExecution error:", e)
        SetAssistantStatus("Available...")
        return False

def BackendLoop():
    gui_p = subprocesses[0] if subprocesses else None
    
    while True:
        try:
            # Check if GUI is alive
            if gui_p and gui_p.poll() is not None:
                # GUI has crashed/exited. Fallback to terminal mode.
                print("\nGUI process has terminated. Switching to Terminal Input Mode.")
                # Force status to True so MainExecution runs
                MainExecution()
                continue
            
            UserInputPath = PROJECT_ROOT / "Data" / "UserInput.data"
            
            # Run MainExecution only if there is pending User Input
            if UserInputPath.exists() and UserInputPath.stat().st_size > 0:
                MainExecution()
            else:
                AIStatus = GetAssistantStatus()
                if "Available..." in AIStatus:
                    sleep(0.1)
                else:
                    SetAssistantStatus("Available...")
        except Exception as e:
            print("BackendLoop error:", e)
            sleep(0.5)

def LaunchGUI():
    print("Launching GUI...")
    gui_path = PROJECT_ROOT / "Frontend" / "GUI.py"
    try:
        # Pass current environment to subprocess to ensure it inherits PATH and VENV variables
        env = os.environ.copy()
        p = subprocess.Popen([sys.executable, str(gui_path)], cwd=PROJECT_ROOT, env=env)
        subprocesses.append(p)
        return p
    except Exception as e:
        print("Failed to launch GUI subprocess:", e)
        return None

if __name__ == '__main__':
    # Start Backend in a thread (so we can monitor subprocesses in main, or vice versa)
    # gui_process = LaunchGUI()
    print("Backend Started. Logic is ready.")
    # Pre-authenticate for Web Mode
    Authenticated = True
    # Run backend loop in main thread
    try:
        BackendLoop()
    except KeyboardInterrupt:
        pass
    finally:
        # cleanup
        for p in subprocesses:
            p.kill()
