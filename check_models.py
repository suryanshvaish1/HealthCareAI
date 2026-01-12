import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from your .env file
load_dotenv()

def list_active_vision_models():
    # Initialize the client using your API key
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    try:
        # Retrieve a JSON list of all active models from the endpoint
        models = client.models.list()
        
        print("--- Active Vision Models on Your Account ---")
        vision_count = 0
        for model in models.data:
            # Filter for models commonly used for vision tasks
            if "vision" in model.id.lower() or "scout" in model.id.lower() or "maverick" in model.id.lower():
                print(f"Model ID: {model.id}")
                vision_count += 1
        
        if vision_count == 0:
            print("No vision-specific models found. Your account may be restricted to text-only models.")
            
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    list_active_vision_models()