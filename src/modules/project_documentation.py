import os
from src.modules.file_processor import read_pdf, read_docx
from src.modules.gpt import get_ollama_response, get_genai_response
import fnmatch

def summarize_with_ollama(content, filename, gpt_provider, model):
    system_prompt = """
    "You are a helpful assistant who summarizes files. 
    Follow this structure:
    ## Purpose of the Code (if existe element):

    - Brief description of the code's purpose, no code.

    ## Core Logic (if existe element):
    
    - Summary of the main logic implemented, no code.

    ## List libraries (if existe element):

    - All libraries used in the code, no code.

    ---
    Be direct in your responses; do not add comments. 
    """
    print("filename" , filename)
    user_prompt = f"Please provide a concise summary of this content:\n\n{content}"
    
    # Use Ollama to generate the summary with the specified model
    if(gpt_provider == "ollama"):
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        summary = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)

    # Check if the response is a dictionary, which indicates an error
    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n\n**Error**: {summary['error']}\n\n"
    
    # Ensure the summary is returned as a string and properly formatted
    formatted_summary = f"#Summary: {filename}\n\n{summary}\n---\n"
    
    # Return the formatted summary
    return formatted_summary

def summarize_with_ollama_final(content, filename, gpt_provider, model):
    system_prompt = """
    You are a software engineer creating a README.md for GitHub. 
    Summarize using knowledge you have from other open-source projects. 
    Be direct in your responses; do not add comments. 
    Format the response in Markdown, response in Portuguese (Br). 

    Follow this structure README.md:    
    ## What the Project Is (if existe element)

    - This project is a ... 

    ## Dependencies (if existe element)

    - Before you can start using or working with this project, make sure to install the following dependencies:

    ## How to Install (if existe element)

    - To get this project up and running, follow these steps:

    ## How to Use (if existe element)

    - Once you have the project set up, you can start using it in the following ways:

    """
    print("filename final" , filename)

    user_prompt = f"ignore structure that text context:\n\{content}, and create README.md"
    
    if(gpt_provider == "ollama"):
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        summary = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)

    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n\n**Error**: {summary['error']}\n\n"   
    formatted_summary = f"# Summary: {filename}\n\n{summary}"
    return formatted_summary

def get_project_files(directory):
    """
    Recursively gets all files in the provided directory.
    """
    project_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.html', '.css', '.yml')):
                project_files.append(os.path.join(root, file))
    return project_files

def read_and_summarize_file(filepath, gpt_provider ,model):
    """
    Reads a file and returns its summary using the specified model.
    """
    filename = os.path.basename(filepath)
    content = None
    if filepath.endswith('.txt'):
        with open(filepath, 'r') as file:
            content = file.read()
    elif filepath.endswith('.pdf'):
        with open(filepath, 'rb') as file:
            content = read_pdf(file)
    elif filepath.endswith('.docx'):
        with open(filepath, 'rb') as file:
            content = read_docx(file)
    else:
        with open(filepath, 'r') as file:
            content = file.read()    
    return summarize_with_ollama(content, filename, gpt_provider, model)  
    

def generate_documentation(project_path, gpt_provider,  model):
    """
    Generates documentation by summarizing each file in the project directory with the selected model,
    ignoring files that match any pattern in ignore_files.
    """
    documentation = []
    project_files = get_project_files(project_path)
    
    # Patterns to ignore
    ignore_patterns = ["project_documentation.txt", "README.md", "*.pyc"]
    
    for file_path in project_files:
        file_name = os.path.basename(file_path)
        
        # Skip files that match any pattern in ignore_patterns
        if any(fnmatch.fnmatch(file_name, pattern) for pattern in ignore_patterns):
            continue

        summary = read_and_summarize_file(file_path, gpt_provider , model)
        documentation.append(summary)
    
    return "\n".join(documentation)
