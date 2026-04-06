from googlesearch import search  # Google search import
from groq import Groq  # Groq client
from json import load, dump  # For reading/writing JSON
import datetime  # For real-time info
from dotenv import dotenv_values  # To load environment variables
import os

# Load environment variables from .env
env_vars = dotenv_values(".env")

# Retrieve variables
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIkey = env_vars.get("GroqAPIkey")

# Initialize Groq client
client = Groq(api_key=GroqAPIkey)

# System instruction (placeholder)
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname}.
*** PROVIDE SHORT, CONCISE, AND DIRECT ANSWERS. ***
*** DO NOT use filler phrases like "Based on the search results" or "The information is...". ***
*** Just state the answer directly. ***
"""

# Try to load chat log from JSON file
# Try to load chat log from JSON file
messages = []
try:
    chatlog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "ChatLog.json"))
    with open(chatlog_path, "r") as f:
        messages = load(f)
except:
    chatlog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "ChatLog.json"))
    with open(chatlog_path, "w") as f:
        dump([], f)

import requests
from bs4 import BeautifulSoup

# Function to fetch content from a URL
def GetWebsiteContent(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract all visible text, not just paragraphs
            text = soup.get_text(separator=' ', strip=True)
            return text[:4000] # Increased limit to capture more context
    except Exception:
        pass
    return ""

# Google search function
def GoogleSearch(query):
    results = list(search(query, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    
    # Try to get content from the first few viable results
    content_found = False
    for url in results:
        # Skip Youtube/Videos as they are hard to scrape text from mostly
        if "youtube.com" in url or "facebook.com" in url:
            continue
            
        content = GetWebsiteContent(url)
        if content:
            Answer += f"Source: {url}\nContent: {content}\n"
            content_found = True
            break # Stop after finding one good source to keep it fast and focused
            
    if not content_found:
        Answer += "No readable content found in search results.\n"
        
    Answer += "[end]"
    return Answer

import re

# Clean answer by removing empty lines and meta-text
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    
    # Remove common meta-commentary
    patterns = [
        r"The search results for .*? are:",
        r"Based on the reference provided,.*",
        r"Based on the provided.*",
        r"I will use it to answer.*",
        r"\[start\]",
        r"\[end\]",
    ]
    
    for pattern in patterns:
        modified_answer = re.sub(pattern, "", modified_answer, flags=re.IGNORECASE).strip()
        
    return modified_answer

# Predefined chatbot messages
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Real-time date and time info
def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data

# Main function to handle response
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Direct handling for time/date queries to avoid LLM fluff
    prompt_lower = prompt.lower()
    if "time" in prompt_lower and "what" in prompt_lower:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}."
    if "date" in prompt_lower and "what" in prompt_lower:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is {current_date}."

    # Truncate messages to avoid 413 Rate Limit (Token Overflow)
    # Keep System prompt (index 0) and the last 6 messages
    if len(messages) > 7:
        messages = [messages[0]] + messages[-6:]

    messages.append({"role": "user", "content": f"{prompt}"})

    # Append search result and info
    # Append search result and info
    google_data = GoogleSearch(prompt)
    messages.append({"role": "user", "content": f"{prompt}\n\nUse this reference:\n{google_data}"})
    

    MAX_HISTORY = 5  # Send only last 5 messages to avoid token overflow
    recent_messages = messages[-MAX_HISTORY:]

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": Information()}] + recent_messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True
    )


    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save updated chat log
    chatlog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "ChatLog.json"))
    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)

    # Remove system message
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

# Main entry loop
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))