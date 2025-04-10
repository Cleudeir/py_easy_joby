import os
import time
import ollama
from typing import Union
import requests




# Import environment variables at the start
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL")
MODEL_OLLAMA: str = os.getenv("MODEL_OLLAMA")
MODEL_OLLAMA_VISION: str = os.getenv("MODEL_OLLAMA_VISION")
MODEL_EMBEDDING_OLLAMA: str = os.getenv("MODEL_EMBEDDING_OLLAMA")


# Setup Ollama client with environment URL
client = ollama.Client(
    host=OLLAMA_BASE_URL, headers={"x-some-header": "some-value"}
)

# Type annotation for the response from Ollama and Google Generative AI
Response = Union[str, dict]

# Function to send an image to Ollama's vision model, along with system and user prompts
import ollama
from typing import List

def send_image_to_ollama(system_prompt: str, user_prompt: str, images_path: str) -> str:
    start_time = time.time()
    try:
        url = f"{OLLAMA_BASE_URL}/api/generate"  # Updated API endpoint
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_OLLAMA_VISION,  # Replace with the model you're using
            "prompt": f"{system_prompt}\n{user_prompt}",
            "stream": False,
            "images": [images_path]
        }        
        # Check if the Ollama model exists
        check_ollama_model_exists(MODEL_OLLAMA_VISION) 
        # Send POST request to the provided API endpoint
        response = requests.post(url, json=payload, headers=headers)
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            text = response_data.get("response", '')
            # Extract text after </think>
            if "</think>" in text:
                text_after_think = text.split("</think>")[1]
                text = text_after_think            
            return text
        else:
            return f"Request failed: {response.status_code} - {response.reason}"
    
    except Exception as e:      
        return f"Request failed: {e}"
    finally:
        end_time = time.time()


# Function to get a response from an Ollama model
def get_ollama_text(system_prompt: str, user_prompt: str) -> dict:
    print("get_ollama_text")
    start_time = time.time()
    try:
        url = f"{OLLAMA_BASE_URL}/api/generate"  # Updated API endpoint
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_OLLAMA,  # Replace with the model you're using
            "prompt": f"{system_prompt}\n{user_prompt}",
            "stream": False        
        }
        
        # Check if the Ollama model exists
        check_ollama_model_exists(MODEL_OLLAMA) 
        # Send POST request to the provided API endpoint with a 60-second timeout
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            text = response_data.get("response", '')
            # Extract text after </think>
            if "</think>" in text:
                text_after_think = text.split("</think>")[1]
                text = text_after_think            
            return text
        else:
            return f"Request failed: {response.status_code} - {response.reason}"
    
    except requests.Timeout:
        return "Request failed: Timeout after 60 seconds"
    except Exception as e:      
        return f"Request failed: {e}"
    finally:
        end_time = time.time()


# Function to get embeddings from an Ollama model
def get_ollama_embeddings(text_input: str) -> Union[list, dict]:
    try:
        check_ollama_model_exists(MODEL_EMBEDDING_OLLAMA)
        # Call ollama.embed with the specified model and input text
        response = ollama.embed(model=MODEL_EMBEDDING_OLLAMA, input=text_input)
        # Extract and return the embeddings
        embeddings = response["embeddings"]
        return embeddings
    except Exception as e:
        return f"error: str({e})"

# Function to check if an Ollama model exists
def check_ollama_model_exists(model_name: str) -> bool:
    try:
        # Fetch available models using ollama.list
        response = client.list()
        models = response.get("models", [])  # Extract models from the response
        # Return True if the model exists in the list
        model_names = [model["name"] for model in models]
        if(model_name in model_names):     
         return True
        else:        
         client.pull(model=model_name, stream=False).wait()
         return False
    except Exception as e:
        return False
