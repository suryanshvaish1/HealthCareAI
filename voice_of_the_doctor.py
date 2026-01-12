import os
import platform
import subprocess
from dotenv import load_dotenv
from gtts import gTTS
from elevenlabs.client import ElevenLabs
import elevenlabs

# Load environment variables from .env file
load_dotenv()

# Get the API Key - ensuring the name matches your .env file exactly
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def play_audio(output_filepath):
    """Helper function to handle cross-platform audio playback"""
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Using start command for mp3 as SoundPlayer often expects .wavpython
            os.startfile(output_filepath)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

def text_to_speech_with_gtts(input_text, output_filepath):
    """Fallback TTS using Google Text-to-Speech"""
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    play_audio(output_filepath)
    return output_filepath

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """Main TTS using ElevenLabs"""
    # Initialize client inside the function to ensure it uses the latest key
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    try:
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2_5"
        )
        
        # Save using the client-compatible method
        elevenlabs.save(audio, output_filepath)
        
        # Autoplay the result
        play_audio(output_filepath)
        
        return output_filepath
    except Exception as e:
        print(f"ElevenLabs Error: {e}")
        # Optional: fallback to gTTS if ElevenLabs fails (e.g., out of credits)
        return text_to_speech_with_gtts(input_text, output_filepath)

# Testing block (uncomment to test standalone)
# if __name__ == "__main__":
#     test_text = "Hi this is Ai with Hassan, testing the integrated system!"
#     text_to_speech_with_elevenlabs(test_text, "final_test.mp3")