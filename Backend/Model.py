import os
from dotenv import dotenv_values
from groq import Groq
from rich import print

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIkey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Define function keywords
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# Preamble / System Instructions
SystemInstruction = """
You are a very accurate Decision-Making Model.
You will decide whether a query is 'general', 'realtime', or a specific task.
*** Do not answer the query, just categorize it. ***

Format:
- 'general [query]': For conversational/knowledge queries (e.g. "general who was akbar?"). SUBSTITUTE [query] with the actual question.
- 'realtime [query]': For queries needing live data (e.g. "realtime who is PM of India?"). SUBSTITUTE [query] with the actual question.
- 'open [app name]': e.g. "open facebook", "open chrome".
- 'close [app name]': e.g. "close notepad", "close telegram".
- 'play [song name]': e.g. "play hello", "play saiyara".
- 'generate image [prompt]': e.g. "generate image of a cat".
- 'reminder [time info]': e.g. "reminder 9pm meeting".
- 'system [task]': e.g. "system mute", "system volume up".
- 'content [topic]': e.g. "content write a mail", "content draft a letter", "content create a poem". Use this for any task asking to write, compose, draft, or create text.
- 'google search [topic]': e.g. "google search python".
- 'youtube search [topic]': e.g. "youtube search tutorials".

If multiple tasks: "open facebook, close whatsapp".
If unsure: "general [actual query content]".
If exit: "exit".

*** Rules for mapping: ***
1. If user says "Quit [App Name]", map it to "close [App Name]".
2. If user says "Quit" (standalone), map it to "exit".
3. If user says "Play [Song Name]", map it to "play [Song Name]".
4. If user asks a Question, map it to "general [Question]" or "realtime [Question]".

*** IMPORTANT: Do not add commas inside the command arguments. ***
*** Correct: "play saiyara", "open visual studio code" ***
*** Incorrect: "play ,saiyara", "open, visual studio code" ***
*** Do not add any explanations or notes. Just the formatted list. ***
"""

# History
messages = []

def FirstLayerDMM(prompt: str = "test"):
    try:
        # Prepare messages includes system instruction + history
        all_messages = [{"role": "system", "content": SystemInstruction}]
        
        # Add recent context (simplified)
        for msg in messages[-4:]:
            all_messages.append(msg)
            
        all_messages.append({"role": "user", "content": prompt})

        # Call Groq
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=all_messages,
            temperature=0.7,
            max_tokens=200,
            stream=False
        )
        
        response = completion.choices[0].message.content.strip()
        
        # Log to history
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "assistant", "content": response})

        # Process response (same logic as before)
        response = response.replace("\n", " ")
        tasks = response.split(",")
        tasks = [i.strip() for i in tasks]

        filtered_tasks = []
        for task in tasks:
            for func in funcs:
                if task.lower().startswith(func):
                    filtered_tasks.append(task)
        
        return filtered_tasks if filtered_tasks else [f"general {prompt}"]

    except Exception as e:
        print(f"DMM Error: {e}")
        return [f"general {prompt}"]

if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        print(FirstLayerDMM(user_input))
