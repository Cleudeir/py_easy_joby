import ollama
import json

def get_available_models():
    try:
        # Use the ollama.list() function to fetch available models
        response = ollama.list()
        models = response.get('models', [])  # Extract models from the response
        model_names = [model['name'] for model in models]  # Get the model names
        return model_names
    except Exception as e:
        return {"error": str(e)}

def get_ollama_response(model, system_prompt, user_prompt):
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    
    try:
        # Call ollama.chat with the model and messages
        response = ollama.chat(model=model, messages=messages)
        # Return the response content directly without using json.dumps
        response_message = response['message']['content']
        return response_message
    except Exception as e:
        return {"error": str(e)}