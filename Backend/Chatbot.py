from groq import Groq # Importing the Groq library to use its API.
from json import load, dump # Importing functions to read and write JSON files.
from datetime import datetime # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values # Importing dotenv_values to read environment variables from a .env file.
import os

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIkey = env_vars.get("GroqAPIkey")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIkey) 

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provides context to the AI chatbot about its role and behavior.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
*** You represent the internal thought process of the Assistant. ***
*** IMPORTANT: The user prefers answers in VOICE format. Keep your responses CONCISE, SHORT, and DIRECT so they can be spoken quickly. Avoid long paragraphs. ***
"""

# A list of system instructions for the chatbot.
SystemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load the chat log from a JSON file.
# Attempt to load the chat log from a JSON file.
try:
    chatlog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "ChatLog.json"))
    with open(chatlog_path, "r") as f:
        messages = load(f)  # Load existing messages from the chat log.
except FileNotFoundError:
    # If the file doesn't exist, create an empty JSON file to store chat logs.
    chatlog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "ChatLog.json"))
    with open(chatlog_path, "w") as f:
        dump([], f)

# Function to get real-time date and time information.
def RealtimeInformation():
    current_date_time = datetime.now()  # Get the current date and time.
    day = current_date_time.strftime("%A")  # Day of the week.
    date = current_date_time.strftime("%d")  # Day of the month.
    month = current_date_time.strftime("%B")  # Full month name.
    year = current_date_time.strftime("%Y")  # Year.
    hour = current_date_time.strftime("%H")  # Hour in 24-hour format.
    minute = current_date_time.strftime("%M")  # Minute.
    second = current_date_time.strftime("%S")  # Second.

    # Format the information into a string.
    data = f"Please use this real-time information if needed.\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours:{minute} minutes:{second} seconds.\n"
    return data

import re

# Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split('\n')  # Split the response into lines.
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines.
    modified_answer = '\n'.join(non_empty_lines)  # Join the cleaned lines back together.
    
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

# Main chatbot function to handle user queries.
def ChatBot(Query):
    """This function sends the user's query to the chatbot and returns the AI's response."""
    
    try:
        # Load the existing chat log from the JSON file.
        chatlog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "ChatLog.json"))
        with open(chatlog_path, "r") as f:
            messages = load(f)

        # Truncate messages to avoid 413 Rate Limit
        if len(messages) > 6:
            messages = messages[-6:]

        # Append the user's query to the messages list.
        messages.append({"role": "user", "content": f"{Query}"})

        # Make a request to the Groq API for a response.
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Specify the AI model to use.
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,  # Include system instructions and chat history.
            max_tokens=1024,  # Limit the maximum tokens in the response.
            temperature=0.7,  # Adjust response randomness (higher means more random).
            top_p=1,  # Use nucleus sampling to control diversity.
            stream=True,  # Enable streaming response.
            stop=None  # Allow the model to determine when to stop.
        )

        Answer = ""   # Initialize an empty string to store the AI's response.

        # Process the streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check if there's content in the current chunk.
                Answer += chunk.choices[0].delta.content  # Append the content to the answer.

        Answer = Answer.replace("</s>", "")  # Clean up any unwanted tokens from the response.

        # Append the chatbot's response to the messages list.
        messages.append({"role": "assistant", "content": Answer})

        # Save the updated chat log to the JSON file.
        chatlog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "ChatLog.json"))
        with open(chatlog_path, "w") as f:
            dump(messages, f, indent=4)

        # Return the formatted response.
        return AnswerModifier(Answer=Answer)

    except Exception as e:
        # Handle errors by printing the exception and resetting the chat log.
        print(f"Error: {e}")
        chatlog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "ChatLog.json"))
        with open(chatlog_path, "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)  # Retry the query after resetting the log.

# Main program entry point.
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")  # Prompt the user for a question.
        print(ChatBot(user_input))  # Call the chatbot function and print its response.