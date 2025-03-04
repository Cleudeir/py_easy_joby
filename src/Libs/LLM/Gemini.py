import base64
import mimetypes
import os
import google.generativeai as genai  # M
import time
from typing import List, Union
from src.Libs.LLM.Gemini_limiter import can_make_request, increment_request_count

# Import environment variables at the start
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "")

# Type annotation for the response from Ollama and Google Generative AI
Response = Union[str, dict]

# Function to get a response from Google Generative AI with model, system, and user prompts
def get_genai_text(system_prompt: str, user_prompt: str) -> Response:
    if not can_make_request():
        return "Request failed: Gemini daily request limit reached. Try again tomorrow."
    start_time = time.time()
    try:
        # Configure the API key
        genai.configure(api_key=GEMINI_API_KEY)
        # Define the generation configuration
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Create the generative model with the specified configuration and system instruction
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=generation_config,
            system_instruction=system_prompt,
        )

        # Start a chat session
        chat_session = model.start_chat(history=[])

        # Send the user prompt and return the response
        response = chat_session.send_message(user_prompt)
        increment_request_count()
        return response.text
    except Exception as e:
        return f"Request failed: {e}"
    finally:
        end_time = time.time()
        print(f"Time gemini model {GEMINI_MODEL}: {(end_time - start_time).__round__(2)} seconds")

def upload_base64_image(base64_string, file_name="image.jpeg", mime_type="image/jpeg"):
    """Decodes base64 string and uploads the image to Gemini."""
    image_data = base64.b64decode(base64_string)
    temp_path = f"/tmp/{file_name}"  # Temporary file path
    
    with open(temp_path, "wb") as f:
        f.write(image_data)
    
    file = genai.upload_file(temp_path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def send_image_to_gemini(system_prompt: str, user_prompt: str, images_path: str) -> Union[str, str]:

    try:
        genai.configure(api_key=GEMINI_API_KEY)

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=generation_config,
            system_instruction=system_prompt,
        )
        file = upload_base64_image(images_path)        
        history = [
            {
                "role": "user",
                "parts": [file],
            },
            {
                "role": "user",
                "parts": [user_prompt],
            },
        ]

        chat_session = model.start_chat(history=history)

        response = chat_session.send_message('create')

        return response.text

    except Exception as e:
        return f"Request failed: {e}"