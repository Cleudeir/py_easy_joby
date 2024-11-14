
import re
from src.modules.gpt import get_ollama_response, get_genai_response
import json

def get_agent_summary(gpt_provider, model, file_content):  
    system_prompt  = "You are a software engineer."    
    user_prompt = f"""
    summarize the code, explain in detail, but not use code in the response, not use exemple.
    that summary will are by to create code:
    {file_content}
    """
    # Use Ollama to generate the summary with the specified model
    if(gpt_provider == "ollama"):
        data = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        data = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)
    print(data)
    # Check if the response is a dictionary, which indicates an error
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    # Return the formatted summary
    return data

def get_agent_coder(gpt_provider, model, summary):   
    system_prompt  = "You are a software engineer."
    summary = f"""
    create code using that summary of the code:
    {summary}
    only create code, no comments, no explanation, only code. create with perfect indentation.
    """
    # Use Ollama to generate the summary with the specified model
    if(gpt_provider == "ollama"):
        data = get_ollama_response(model, system_prompt, summary)
    elif(gpt_provider == "gemini"):
        data = get_genai_response(system_prompt=system_prompt, user_prompt=summary)
    print(data)
    # Check if the response is a dictionary, which indicates an error
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    # Return the formatted summary
    # Regular expression to match the content inside the curly braces {}
    regex = r"```[a-zA-Z]+\n([\s\S]*?)```"
    # Find all matches
    matches = re.findall(regex, data)
    print('matches',matches)
    # Extract and print only the content inside the curly braces
    for content in matches:
        # Removing leading and trailing spaces
        return content.strip().replace('<', '&lt;')

def get_agent_score(gpt_provider, model, file_content, summary):   
    system_prompt  = "You are a software engineer."
    summary =f"""    
    reconstruction:
    {summary}
    Original:
    {file_content}
    
    compare if "reconstruction" is similar "original" code, to be critical, analyze all points.
    
    Provide a score between 0 and 1000, where a higher number indicates greater similarity and a lower number indicates less similarity.    
    Respond only with a JSON object formatted as follows:
    {{
        "score": number
    }}
    only create score, no comments, no explanation.
    """
    # Use Ollama or Gemini to generate the summary with the specified model
    if gpt_provider == "ollama":
        data = get_ollama_response(model, system_prompt, summary)
    elif gpt_provider == "gemini":
        data = get_genai_response(system_prompt=system_prompt, user_prompt=summary)
    
    # Check if the response is a dictionary, which indicates an error
    if isinstance(data, dict) and "error" in data:
        return {"error": data["error"]}
    
    # Parse the response as JSON if possible
    try:
        print(data,json.loads(data))
        return json.loads(data)
    except json.JSONDecodeError:
        return {"score": 0}


def get_agent_improvement(gpt_provider, model, file_content, summary, score):  
    system_prompt = "You are a software engineer."
    summary = f"""
    other engineers have provided a summary the code.
    that summary is available in {score} points, between 0 and 1000, where a higher number indicates greater similarity and a lower number indicates less similarity.
    
    use original code: 
    {file_content}
    and summary you co-worker:
    {summary}
    
    now you need summarize the original code, explain in detail, but not use code in the response, create better summary you co-worker.
    {file_content}
    """
    # Use Ollama to generate the summary with the specified model
    if(gpt_provider == "ollama"):
        data = get_ollama_response(model, system_prompt, summary)
    elif(gpt_provider == "gemini"):
        data = get_genai_response(system_prompt=system_prompt,user_prompt=summary)
    print(data)
    # Check if the response is a dictionary, which indicates an error
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    # Return the formatted summary
    return data