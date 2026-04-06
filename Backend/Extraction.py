from groq import Groq
from json import load
from dotenv import dotenv_values
import os

env_vars = dotenv_values(".env")
GroqAPIkey = env_vars.get("GroqAPIkey")

client = Groq(api_key=GroqAPIkey)

def Extraction():
    try:
        chatlog_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "ChatLog.json"))
        with open(chatlog_path, "r") as f:
            messages = load(f)
        
        # Use last 10 messages for context, or all if less
        context = messages[-10:] if len(messages) > 10 else messages
        
        prompt = f"""
        Analyze the following conversation history and extract the key information.
        Provide a summary of:
        1. Important Dates/Times mentioned.
        2. Key Tasks or Action Items.
        3. Important Definitions or Facts discussed.
        
        Format the output as a clean bulleted list.
        
        Conversation:
        {context}
        """
        
        completion = client.chat.completions.create(
            # model="llama3-8b-8192",
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.5
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Extraction failed: {e}"
