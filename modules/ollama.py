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
    # This is how to use the ollama.chat API with messages
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
        # If necessary, decode any escaped Unicode characters in the response
        response_message = json.dumps(response['message']['content'], ensure_ascii=False)
        return response_message  # Return the response content with special characters properly handled
    except Exception as e:
        return {"error": str(e)}
