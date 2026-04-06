import subprocess   # Used to open and close applications, run system commands
import webbrowser   # For opening URLs in default browser
import requests     # To perform HTTP requests
import asyncio      # For asynchronous operations
try:
    from pywhatkit import search, playonyt  # For Google search and YouTube playback
except Exception as e:
    print(f"Failed to import pywhatkit: {e}. Automation features may be limited.")
    def search(topic): print("Google search unavailable")
    def playonyt(topic): print("YouTube play unavailable")
from dotenv import dotenv_values        # For loading environment variables from .env
from bs4 import BeautifulSoup           # To parse HTML and extract links
from groq import Groq                   # For AI-generated content (Groq client)
import os                               # OS-level functions (like env)

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIkey = env_vars.get('GroqAPIkey')

# Define headers and client
useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
client = Groq(api_key=GroqAPIkey)

# Chatbot initial prompt and history
messages = []
SystemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {os.environ.get('USER', 'AI Assistant')}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."
}]

# Extract useful URLs from Google results
def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith("/url?q="):
            return [href.split("/url?q=")[1].split("&")[0]]
    return []

# Perform Google search and return raw HTML
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": useragent}
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

# Perform Google search (in browser)
def GoogleSearch(Topic):
    search(Topic)
    return True

# YouTube search (in browser)
def YouTubeSearch(Topic):
    webbrowser.open(f"https://www.youtube.com/results?search_query={Topic}")
    return True

# Play YouTube video directly
def PlayYoutube(query):
    playonyt(query)
    return True

# Use Groq AI to generate content
def ContentWriterAI(prompt):
    messages.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=SystemChatBot + messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )

 # Process the streamed response
    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

 # Clean up the response
    Answer = Answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    return Answer

# Generate content and save as text file
def Content(Topic):
    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)
    file_path = f"Data/{Topic.lower().replace(' ', '')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
    subprocess.call(["open", file_path])  # macOS open default text editor
    return True

# Open app on Mac, fallback to browser if not found
def OpenApp(app_name):
    try:
        # 1. First try direct path (handles .app folder names)
        app_path_guess = f"/Applications/{app_name}.app"
        if os.path.exists(app_path_guess):
            subprocess.Popen(["open", app_path_guess])
            print(f"[✓] Opened (path): {app_name}")
            return True

        # 2. Try with Spotlight via mdfind (case-insensitive match)
        result = subprocess.run(
            ["mdfind", f'kMDItemKind == "Application" && kMDItemDisplayName ==[c] "{app_name}"'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        app_paths = result.stdout.strip().split('\n')
        if app_paths and app_paths[0]:
            subprocess.Popen(["open", app_paths[0]])
            print(f"[✓] Opened (mdfind): {app_name}")
            return True

        # 3. Try again with Title Case (in case user typed lowercase like 'whatsapp')
        title_case = app_name.title()
        result = subprocess.run(
            ["mdfind", f'kMDItemKind == "Application" && kMDItemDisplayName ==[c] "{title_case}"'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Check if any apps were found
        app_paths = result.stdout.strip().split('\n')
        if app_paths and app_paths[0]:
            subprocess.Popen(["open", app_paths[0]])
            print(f"[✓] Opened (mdfind title case): {title_case}")
            return True

        # If not found, fallback to Google
        raise FileNotFoundError

# If all else fails, search Google for the app
    except Exception:
        print(f"[✗] App '{app_name}' not found on system. Trying in browser...")
        # Direct web fallbacks for common apps to save time
        web_apps = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "whatsapp": "https://web.whatsapp.com",
            "twitter": "https://twitter.com",
            "x": "https://x.com",
            "linkedin": "https://www.linkedin.com",
            "gmail": "https://mail.google.com"
        }
        
        lower_name = app_name.lower().strip()
        if lower_name in web_apps:
            webbrowser.open(web_apps[lower_name])
            print(f"[✓] Opened in browser (Direct): {web_apps[lower_name]}")
            return True

        html = search_google(app_name)
        if html:
            links = extract_links(html)
            if links:
                webbrowser.open(links[0])
                print(f"[✓] Opened in browser: {links[0]}")
                return True
        webbrowser.open(f"https://www.google.com/search?q={app_name}")
        print(f"[!] Fallback Google search opened: {app_name}")
        return False
    
# Close app on Mac
def CloseApp(app_name):
    try:
        # Try closing app using AppleScript directly
        result = subprocess.run(
            ["osascript", "-e", f'tell application "{app_name}" to quit'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

# Check if the command was successful
        if result.returncode == 0:
            print(f"[✓] Closed {app_name}")
            return True
        else:
            print(f"[✗] Failed to close {app_name}. It may not be running or name is incorrect.")
            return False
        # If the app is not found, try using Activity Monitor
    except Exception as e:
        print(f"[✗] Error trying to close {app_name}: {e}")
        return False


# Control macOS volume via AppleScript
def System(command):
    if command == "mute":

        subprocess.call(["osascript", "-e", 'set volume output muted true'])
    elif command == "unmute":

        subprocess.call(["osascript", "-e", 'set volume output muted false'])
    elif command == "volume up":

        subprocess.call(["osascript", "-e", 'set volume output volume ((output volume of (get volume settings)) + 10)'])
    elif command == "volume down":

        subprocess.call(["osascript", "-e", 'set volume output volume ((output volume of (get volume settings)) - 10)'])
    return True

# Convert user commands into function execution
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)

        else:
            print(f"No Function Found. For: {command}")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

#Automation function to handle multiple commands

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

# # Test commands
# if __name__ == "__main__":
#     sample_commands = [
#             "open calculator",
#             "open whatsapp"
#     ]
#     Automation(sample_commands)
