import os
import ollama
import google.generativeai as genai  # M


client = ollama.Client(
    host="https://api.apps.tec.br/ollama", headers={"x-some-header": "some-value"}
)


# Function to get a response from Google Generative AI with model, system, and user prompts
def get_genai_response(system_prompt, user_prompt):
    try:
        model_name = "gemini-1.5-flash"
        # Configure the API key
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
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
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_prompt,
        )

        # Start a chat session
        chat_session = model.start_chat(history=[])

        # Send the user prompt and return the response
        response = chat_session.send_message(user_prompt)
        return response.text
    except Exception as e:
        return {"error": str(e)}


# Function to get available models from Ollama
def get_ollama_models():
    try:
        # Fetch available models using ollama.list
        response = client.list()
        models = response.get("models", [])  # Extract models from the response
        model_names = [model["name"] for model in models]  # Get the model names
        return model_names
    except Exception as e:
        return {"error": str(e)}


def get_ollama_vision_models():
    try:
        # Fetch available models using ollama.list
        response = client.list()
        models = response.get("models", [])  # Extract models from the response
        # Filter models with name vision or llava
        models = [
            model
            for model in models
            if "vision" in model["name"].lower() or "llava" in model["name"].lower()
        ]
        # return only names
        models = [model["name"] for model in models]

        return models
    except Exception as e:
        return {"error": str(e)}


# Function to get a response from an Ollama model
def get_ollama_response(model_name, system_prompt, user_prompt):
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        # Call ollama.chat with the specified model and messages
        response = ollama.chat(model=model_name, messages=messages)
        # Return the response content directly
        response_message = response["message"]["content"]
        return response_message
    except Exception as e:
        return {"error": str(e)}


# Function to get embeddings from an Ollama model
def get_ollama_embeddings(model_name, text_input):
    try:
        # Call ollama.embedding with the specified model and input text
        response = ollama.embed(model=model_name, input=text_input)
        # Extract and return the embeddings
        embeddings = response["embeddings"]
        return embeddings
    except Exception as e:
        return {"error": str(e)}
