import os
import ollama
import re
from typing import Union
import requests




# Import environment variables at the start
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL")
print('------------')
print('Ollama Variables\n')
print(OLLAMA_BASE_URL)
MODEL_OLLAMA: str = os.getenv("MODEL_OLLAMA")
print(MODEL_OLLAMA)
MODEL_OLLAMA_VISION: str = os.getenv("MODEL_OLLAMA_VISION")
print(MODEL_OLLAMA_VISION)
MODEL_EMBEDDING_OLLAMA: str = os.getenv("MODEL_EMBEDDING_OLLAMA")
print(MODEL_EMBEDDING_OLLAMA)
print('------------')

# Setup Ollama client with environment URL
client = ollama.Client(
    host=OLLAMA_BASE_URL, headers={"x-some-header": "some-value"}
)

# Type annotation for the response from Ollama and Google Generative AI
Response = Union[str, dict]

# Function to send an image to Ollama's vision model, along with system and user prompts
def send_image_to_ollama(system_prompt: str, user_prompt: str, images_path:  list[str]) -> Response:
    try:
        # Prepare the image and messages to send to Ollama
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt, 'images': images_path},
        ]
        check_ollama_model_exists(MODEL_OLLAMA_VISION)        
        # Call ollama.chat with the vision model and messages (assuming a vision-enabled model)
        response = ollama.chat(model=MODEL_OLLAMA_VISION, messages=messages)
        # Return the response content directly
        response_message = response["message"]["content"]
        return response_message
    except Exception as e:
        return {"error": str(e)}


# Function to get a response from an Ollama model
def get_ollama_text(system_prompt: str, user_prompt: str) -> dict:
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
        
        # Send POST request to the provided API endpoint
        response = requests.post(url, json=payload, headers=headers)
       
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            text = response_data.get("response", '')
            print("Original text:", text)

            # Extract text after </think>

            if "</think>" in text:
                text_after_think = text.split("</think>")[1]
                text = text_after_think               
            
            return text
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
    
    except Exception as e:
        print(e)
        return {"error": str(e)}



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
        return {"error": str(e)}

# Function to check if an Ollama model exists
def check_ollama_model_exists(model_name: str) -> bool:
    try:
        # Fetch available models using ollama.list
        response = client.list()
        models = response.get("models", [])  # Extract models from the response
        # Return True if the model exists in the list
        model_names = [model["name"] for model in models]
        print(model_names)
        if(model_name in model_names):     
         return True
        else:        
         client.pull(model=model_name, stream=False).wait()
         return False
    except Exception as e:
        return False
