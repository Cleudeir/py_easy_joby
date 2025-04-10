import os
import time
from typing import Union
from src.Libs.LLM.Gemini import get_genai_text, send_image_to_gemini
from src.Libs.LLM.Ollama import get_ollama_embeddings, get_ollama_text, send_image_to_ollama

# Import environment variables at the start
# PROVIDER
PROVIDER: str = os.getenv("PROVIDER")

# Type annotation for the response from Ollama and Google Generative AI
Response = Union[str, dict]

def get_text(system_prompt: str, user_prompt: str) -> Response:
    if PROVIDER == "gemini":
        time.sleep(4)
        text = get_genai_text(system_prompt, user_prompt)
        if("Request failed" in text):
             text = get_ollama_text(system_prompt, user_prompt)
        return text
    elif PROVIDER == "ollama":
        text = get_ollama_text(system_prompt, user_prompt)
        if("Request failed" in text):
             text = get_genai_text(system_prompt, user_prompt)
        return text
    else:
        return "Unsupported provider"
    
    
def get_vision(system_prompt: str, user_prompt: str, images_path: str) -> Response:
    if PROVIDER == "gemini":
        time.sleep(4)
        return send_image_to_gemini(system_prompt, user_prompt, images_path)
    elif PROVIDER == "ollama":    
        return send_image_to_ollama(system_prompt, user_prompt, images_path)
    else:
        return "Unsupported provider"
    
    
def get_embeddings(system_prompt: str, user_prompt: str) -> Response:
    if PROVIDER == "gemini":
        time.sleep(4)
        return get_ollama_embeddings(system_prompt, user_prompt)
    elif PROVIDER == "ollama":
        return get_ollama_embeddings(system_prompt, user_prompt)
    else:
        return "Unsupported provider"

def get_provider():
    return PROVIDER
