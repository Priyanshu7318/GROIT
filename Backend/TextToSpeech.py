import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables from a .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-IN-PrabhatNeural") # Get the AssistantVoice from the environment variables

# Asynchronous function to convert text to an audio file with enhanced voice settings
async def TextToAudioFile(text) -> None:
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "speech.mp3"))

    # Check if the file already exists
    if os.path.exists(file_path):
        os.remove(file_path) # If it exists, remove it to avoid overwriting errors
    
    # Create the communicate object with enhanced voice settings
    # Latest edge-tts supports advanced prosody controls: pitch, rate, volume
    communicate = edge_tts.Communicate(
        text, 
        voice=AssistantVoice,
        pitch="+5Hz",           # Pitch adjustment for more natural sound
        rate="+10%",            # Speech rate adjustment
        volume="+0%"           # Volume level adjustment
    )
    await communicate.save(file_path)

# Function to manage text-to-speech (TTS) functionality
def TTS(text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(text))

            # Initialize pygame mixer for audio playback
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Load the generated speech file into pygame mixer
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "speech.mp3"))
            
            # Use try-except for music loading to handle file access issues
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
            except pygame.error as e:
                print(f"Pygame load error: {e}. Retrying fallback...")
                raise e
            
            # Loop until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10) # Limit the loop to 10 ticks per second
            
            # Stop and unload music to release file lock
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            
            return True # Return True if the audio played successfully

        except Exception as e:
            print(f"Error in Edge TTS: {e}")
            print("Attempting fallback to pyttsx3...")
            try:
                import pyttsx3
                engine = pyttsx3.init()
                # Set voice properties for better fallback
                voices = engine.getProperty('voices')
                if voices:
                    engine.setProperty('voice', voices[0].id)
                engine.say(text)
                engine.runAndWait()
                return True
            except Exception as e2:
                print(f"Error in Fallback TTS: {e2}")
                return False

        finally:
            try:
                # Call the provided function with False to signal the end of TTS
                func(False)
            except Exception as e:
                pass

# Function to manage text-to-speech with additional responses for long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split('.') # Split the text by periods into a list of sentences

    # List of predefined responses for cases where the text is too long
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # If the text is very long (more than 10 sentences and 1000 characters), add a response message
    if len(Data) > 10 and len(Text) > 1000:
        TTS(".".join(Text.split(".")[:4]) + "." + random.choice(responses), func)
    # Otherwise, just play the whole text
    else:
        TTS(Text, func)

# Main execution loop
if __name__ == "__main__":
    while True:
        # Prompt user for input and pass it to TextToSpeech function
        TextToSpeech(input("Enter the text: "))