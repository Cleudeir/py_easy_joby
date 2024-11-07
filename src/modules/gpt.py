import os
import ollama
import google.generativeai as genai  # M

# Function to get a response from Google Generative AI with model, system, and user prompts
def get_genai_response(system_prompt, user_prompt):
   
    model_name = "gemini-1.5-flash"
    # Configure the API key
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    print(os.environ["GEMINI_API_KEY"])
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
        system_instruction=system_prompt
    )
    
    # Start a chat session
    chat_session = model.start_chat(history=[])
    
    # Send the user prompt and return the response
    response = chat_session.send_message(user_prompt)
    print(response.text) 
    return response.text

# Function to get available models from Ollama
def get_ollama_models():
    try:
        # Fetch available models using ollama.list
        response = ollama.list()
        models = response.get('models', [])  # Extract models from the response
        model_names = [model['name'] for model in models]  # Get the model names
        return model_names
    except Exception as e:
        return {"error": str(e)}

# Function to get a response from an Ollama model
def get_ollama_response(model_name, system_prompt, user_prompt):
    print("prompt length", len(user_prompt), "system prompt length", len(system_prompt))
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
        # Call ollama.chat with the specified model and messages
        response = ollama.chat(model=model_name, messages=messages)
        # Return the response content directly
        response_message = response['message']['content']
        return response_message
    except Exception as e:
        return {"error": str(e)}

