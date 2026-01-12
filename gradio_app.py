import os
from dotenv import load_dotenv
import gradio as gr

# Load environment variables from .env
load_dotenv()

# Import your custom modules
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# System prompt for the AI Doctor
import os
from dotenv import load_dotenv
import gradio as gr

# Load environment variables from .env
load_dotenv()

# Import your custom modules
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# System prompt for the AI Doctor
SYSTEM_PROMPT = """You are a warm, empathetic, and highly skilled physician. 
Your goal is to make the patient feel heard and cared for. 

When you respond, speak naturally as if we are sitting in a clinic together. 
Do not use robotic headers like '[OBSERVATION]'. Instead, weave your reasoning into a conversation.

Follow this flow:
1. GREETING & EMPATHY: Start by addressing the patient's symptoms with genuine concern (e.g., 'I'm sorry you're dealing with that discomfort...').
2. OBSERVATION & DEDUCTION: Mention what you noticed in the image and how it relates to what they told you (e.g., 'Looking at the photo, that redness near the edge suggests...').
3. PLAN: Offer a clear diagnosis and a gentle recommendation for next steps.

Avoid overly formal transitions like 'Furthermore' or 'Consequently'. Use contractions like 'I've' or 'You're' to sound more human."""

def process_inputs(audio_filepath, image_filepath):
    # 1. Validation
    if audio_filepath is None:
        return "No audio provided", "Please describe your symptoms via audio.", None

    # 2. Speech-to-Text (Patient Voice)
    try:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    except Exception as e:
        return f"STT Error: {str(e)}", "Speech transcription failed.", None

    # 3. Vision Analysis (Doctor's Brain) using the verified active model
    doctor_response = ""
    if image_filepath:
        # We ask the model for its Reasoning Trace
        doctor_response = analyze_image_with_query(
            query=SYSTEM_PROMPT + "\nPatient says: " + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model="meta-llama/llama-4-scout-17b-16e-instruct" 
        ) 
    else:
        doctor_response = "Please provide an image for a full clinical reasoning trace."

    # 4. Text-to-Speech (Doctor's Voice)
    try:
        voice_of_doctor_path = text_to_speech_with_elevenlabs(
            input_text=doctor_response, 
            output_filepath="final.mp3"
        ) 
    except Exception as e:
        # Prevents the UI from hanging if there is a permission error
        print(f"ElevenLabs Error: {e}")
        voice_of_doctor_path = None

    return speech_to_text_output, doctor_response, voice_of_doctor_path

# --- UI Layout matches your previous successful run ---
with gr.Blocks(title="AI Doctor 2.0") as demo:
    gr.Markdown("# 🏥 AI Doctor: Vision & Voice Analysis")
    gr.Markdown("Upload a medical image and explain your symptoms using the microphone.")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Describe Symptoms")
            image_input = gr.Image(type="filepath", label="Medical Image")
            submit_btn = gr.Button("Submit", variant="primary")
            
        with gr.Column():
            stt_output = gr.Textbox(label="Speech to Text")
            response_output = gr.Textbox(label="Doctor's Response")
            voice_output = gr.Audio(label="Doctor's Voice")

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[stt_output, response_output, voice_output]
    )

if __name__ == "__main__":
    demo.launch(debug=True)

def process_inputs(audio_filepath, image_filepath):
    # 1. Validation
    if audio_filepath is None:
        return "No audio provided", "Please describe your symptoms via audio.", None

    # 2. Speech-to-Text (Patient Voice)
    try:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    except Exception as e:
        return f"STT Error: {str(e)}", "Speech transcription failed.", None

    # 3. Vision Analysis (Doctor's Brain) using the verified active model
    doctor_response = ""
    if image_filepath:
        try:
            # Using your active Llama 4 Scout model for fast, accurate vision analysis
            doctor_response = analyze_image_with_query(
                query=SYSTEM_PROMPT + speech_to_text_output,
                encoded_image=encode_image(image_filepath),
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
        except Exception as e:
            print(f"Vision Error: {e}")
            doctor_response = "I encountered an error connecting to my vision systems. Please check your API key."
    else:
        doctor_response = "No image provided for me to analyze."

    # 4. Text-to-Speech (Doctor's Voice)
    try:
        voice_of_doctor_path = text_to_speech_with_elevenlabs(
            input_text=doctor_response, 
            output_filepath="final.mp3"
        ) 
    except Exception as e:
        # Prevents the UI from hanging if there is a permission error
        print(f"ElevenLabs Error: {e}")
        voice_of_doctor_path = None

    return speech_to_text_output, doctor_response, voice_of_doctor_path

# --- UI Layout matches your previous successful run ---
with gr.Blocks(title="AI Doctor 2.0") as demo:
    gr.Markdown("# 🏥 AI Doctor: Vision & Voice Analysis")
    gr.Markdown("Upload a medical image and explain your symptoms using the microphone.")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Describe Symptoms")
            image_input = gr.Image(type="filepath", label="Medical Image")
            submit_btn = gr.Button("Submit", variant="primary")
            
        with gr.Column():
            stt_output = gr.Textbox(label="Speech to Text")
            response_output = gr.Textbox(label="Doctor's Response")
            voice_output = gr.Audio(label="Doctor's Voice")

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[stt_output, response_output, voice_output]
    )

if __name__ == "__main__":
    demo.launch(debug=True)