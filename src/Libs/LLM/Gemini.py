import os
import google.generativeai as genai  # M
import time
from typing import Union
import PIL.Image

# Import environment variables at the start
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "")

# Type annotation for the response from Ollama and Google Generative AI
Response = Union[str, dict]

# Function to get a response from Google Generative AI with model, system, and user prompts
def get_genai_text(system_prompt: str, user_prompt: str) -> Response:
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
     
        return response.text
    except Exception as e:
        return f"error str({e})"
    finally:
        end_time = time.time()
        print(f"Time gemini model {GEMINI_MODEL}: {(end_time - start_time).__round__(2)} seconds")

# Function to send an image to the Gemini model along with system and user prompts
def send_image_to_gemini(system_prompt: str, user_prompt: str, images_path: list[str]) -> Union[str, dict]:
    try:
        # Configure the API key
        genai.configure(api_key=GEMINI_API_KEY)
        for image_path in images_path:
            print(image_path)
            file = genai.upload_file(image_path)
        # Define the generation configuration for Gemini
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Create the generative model with system instruction and image input
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=generation_config,
            system_instruction=system_prompt,
        )
        
        parts = []
        for image_path in images_path:
            file = PIL.Image.open(image_path)
            parts.append(file)
        parts.append(user_prompt)
        
        history=[
            {
                "role": "user",
                "parts": parts,
            },       
        ]
        # Start a chat session
        chat_session = model.start_chat(history=history)

        # Send the user prompt and image data as part of the input
        response = chat_session.send_message('create')

        # Return the response text
        return response.text
    except Exception as e:
        return f"error: str({e})"
 