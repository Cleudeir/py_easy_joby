
import re
from src.modules.gpt import get_ollama_embeddings, get_ollama_response, get_genai_response
import json
from sklearn.metrics.pairwise import cosine_similarity


structure = """
   # File Summary
    ## Language Used and Frameworks
    - **What programming language is used in the file?**
    - Mention any frameworks, libraries, or dependencies used in the file.

    ---
    ## Purpose of the File
    - **What is the primary purpose of this file?**
    - Explain the file's main role within the system and its contribution to the overall functionality.

    ---

    ## Functions and Classes Defined
    - **What are the main functions or classes defined in the file?**
    - List each function or class (name,input,output).

    ---

    ## Execution Flow
    - **What is the hierarchical execution flow of the file?**
    - Describe the sequence in which the functions or classes operate, illustrating how the file executes its intended logic.

    ---
    
    ## Variables and Constants
    - **What are the variables and constants defined in the file?**
    - List each variable or constant along with its purpose and its value.

    ---

    ## Input and Output
    - **What are the inputs and outputs of the file?**

    ## Internal and External Dependencies
    - **What libraries or modules are imported?**
    - Identify the internal or external dependencies and how they integrate into the file's operations.

    ---

    ## Error and Exception Handling
    - **What types of errors are handled?**
    - Outline the error-handling mechanisms present in the file and how they ensure robustness.

    ---

    ## Comments
    - **What comments are present in the file?**
    - Describe the nature and purpose of the comments, such as clarifications, assumptions, or development notes.

    ---

    ## Internal Tests or Checks
    - **What tests or verification mechanisms are included?**
    - Highlight any assertions, tests, or internal validation steps implemented to ensure correctness.
"""

def get_agent_summary(gpt_provider, model, file_content):  
    system_prompt  = "You are a software engineer. will create documentation."    
    user_prompt = f"""
    {file_content}
    
    Summarize that code, explain in detail.
    Not use code in the response, not use exemple.
    Use this structure:
    {structure}
    """
    # Use Ollama to generate the summary with the specified model
    if(gpt_provider == "ollama"):
        data = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        data = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)
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
    only create code, no comments in code, no explanation, only code. create with perfect indentation, create complete code.
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
    # Extract and print only the content inside the curly braces
    for content in matches:
        # Removing leading and trailing spaces
        return content.strip()

def get_agent_similarity(file_content, reconstruct_code):
    embeddings_code = get_ollama_embeddings(model_name='nomic-embed-text:latest', text_input=file_content)
    embeddings_reconstruct_code = get_ollama_embeddings(model_name='nomic-embed-text:latest', text_input=reconstruct_code)
    similaridade = cosine_similarity(embeddings_code, embeddings_reconstruct_code)
    return similaridade[0][0]

def get_agent_improvement(gpt_provider, model, file_content, summary):       
    system_prompt  = "You are a software engineer. will create documentation."
    user_prompt =f"""    
    That is code: 
    {file_content}
    and this is a summary of the code:
    {summary}
    Analyze this summary and appoint the missing and wrong points.
    Response in this structure:
    
    ### Missing:
    * appoint in bullet points.
    ### Wrong:
    * appoint in bullet points.  
      
    flow structure, no comments, no explanation.
    """
    # Use Ollama or Gemini to generate the summary with the specified model
    if gpt_provider == "ollama":
        data = get_ollama_response(model, system_prompt, user_prompt)
    elif gpt_provider == "gemini":
        data = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)
    
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    
    return data

def get_agent_fix_summary(gpt_provider, model, file_content, summary, improvement):  
    system_prompt = "You are a software engineer.  will create documentation"
    user_prompt = f"""
    that is a code:
    {file_content}
    and this a summary of the code:
    {summary}
    rewrite this summary and fix this points
    {improvement}
    Not use code or exemple in the response.
    """
    # Use Ollama to generate the summary with the specified model
    if(gpt_provider == "ollama"):
        data = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        data = get_genai_response(system_prompt=system_prompt,user_prompt=user_prompt)
    # Check if the response is a dictionary, which indicates an error
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    # Return the formatted summary
    return data