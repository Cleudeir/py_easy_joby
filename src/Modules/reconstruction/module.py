
import re
from sklearn.metrics.pairwise import cosine_similarity
from src.Libs.LLM.Provider import get_embeddings, get_text

structure = """
    # File Summary

    ## Language & Frameworks

        Programming language and frameworks used.

    ## Purpose

        Primary goal of the file.

    ## Functions & Classes

        List each function or class with inputs and outputs.

    ## Execution Flow

        Hierarchical execution flow.

    ## Variables & Constants

        List variables/constants with their purpose and values.

    ## Input & Output

        File's inputs and outputs.

    ## Dependencies
        
        Internal and external modules/libraries used.
    """  

def get_agent_summary(file_content):  
    
    system_prompt  = "You are a software engineer. will create documentation."     

    user_prompt = f"""
    {file_content}   
    Summarize that code.
    Use this structure:
    {structure}
    not use code in the response, not use exemple, no comments, no explanation.  
    """
    # Use Ollama to generate the summary with the specified model
    data = get_text(system_prompt, user_prompt)
    
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    # Return the formatted summary
    return data

def get_agent_coder(summary):   
    system_prompt  = "You are a software engineer."
    summary = f"""
    create code using that summary of the code:
    {summary}
    only create code, no comments in code, no explanation, only code. create with perfect indentation, create complete code.
    """
    # Use Ollama to generate the summary with the specified model
    data = get_text( system_prompt, summary)
    # Check if the response is a dictionary, which indicates an error
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    # Return the formatted summary
    # Regular expression to match the content inside the curly braces {}
    regex = r"```[a-zA-Z]+\n([\s\S]*?)```"
    # Find all matches
    matches = re.findall(regex, data)
    # Extract and print only the content inside the curly braces
    for content in matches:
        # Removing leading and trailing spaces
        return content.strip()

def get_agent_similarity(file_content, reconstruct_code):
    embeddings_code = get_embeddings(text_input=file_content)
    embeddings_reconstruct_code = get_embeddings(text_input=reconstruct_code)
    similaridade = cosine_similarity(embeddings_code, embeddings_reconstruct_code)
    return similaridade[0][0]

def get_agent_improvement(file_content, code_generation):       
    system_prompt  = "You are a software engineer. will create documentation."
    user_prompt =f"""    
    That is code a original code:
    {file_content}
    and this is generated code:
    {code_generation}
    Analyze this summary and appoint the missing and wrong points.
    Response in this structure:
    
    ### Missing:
    * appoint in bullet points.
    ### Wrong:
    * appoint in bullet points.  
      
    flow structure, no comments, no explanation.
    """
    # Use Ollama or Gemini to generate the summary with the specified model
    data = get_text(system_prompt, user_prompt)
    
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    
    # Return the formatted summary    
    return data
def get_agent_fix_summary(summary, improvement):  
    system_prompt = "You are a software engineer.  will create documentation"
    user_prompt = f"""  
    That is a summary of the code:
    {summary}
    Attention in this appointment:
    {improvement}
    improve summary using this structure:
    {structure}    
    not use code in the response, not use exemple, no comments, no explanation.
    """
    # Use Ollama to generate the summary with the specified model
    data = get_text(system_prompt, user_prompt)
    # Check if the response is a dictionary, which indicates an error
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    # Return the formatted summary
    return data

def get_agent_fix_code(code, improvement):  
    system_prompt = "You are a software engineer.  will create documentation"
    user_prompt = f"""  
    That is a code:
    {code}
    Attention in this appointment to fix code:
    {improvement}
    response only code, no comments in code, no comments, no explanation.    
    """
    # Use Ollama to generate the summary with the specified model
    data = get_text(system_prompt, user_prompt)
    # Check if the response is a dictionary, which indicates an error
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    # Return the formatted summary
    return data