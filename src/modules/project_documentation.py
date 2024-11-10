import os
import time
from src.modules.file_processor import read_pdf, read_docx
from src.modules.gpt import get_ollama_response, get_genai_response
import fnmatch
from flask import current_app


system_prompt = """
    "You are a helpful assistant who summarizes files. 
    Follow this structure, not create code:
    ## Purpose of the Code\n\n
    * Brief description of the code's purpose.
    ##  Business rule\n\n    
    * Summary of the business rule.
    ## List external libraries\n\n
    (if existe element) 
    * libraries named (little description).
    (else)
    * No libraries used.
    ## fields\n\n
     * fields named (little description).
    (else)
    * No fields used.
    Be direct in your responses; do not add comments. 
    """

def summarize_with_ollama_agent01(content, filename, gpt_provider, model):    
    print("filename" , filename,'\n\n')
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
    formatted_summary = f"# Summary: {filename}\n\n{summary}\n---\n"
    
    # Return the formatted summary
    return formatted_summary


def summarize_with_ollama_agent02(content, gpt_provider, model):
 
    user_prompt = f"{content}\n\nAnalyze if response follow structure and fix if not."
    
    # Use Ollama to generate the summary with the specified model
    if(gpt_provider == "ollama"):
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        summary = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)

    # Check if the response is a dictionary, which indicates an error
    if isinstance(summary, dict) and "error" in summary:
        return f"**Error**: {summary['error']}\n\n"
    # Return the formatted summary
    return summary

def summarize_with_ollama_final(content, filename, gpt_provider, model):
    system_prompt = """
    You are a software engineer creating a README.md for GitHub. 
    Summarize using knowledge you have from other open-source projects. 
    Be direct in your responses; do not add comments. 
    Format the response in Markdown, but not use ```Markdown```. 

    Follow this structure README.md, not create code:  
    ## Project structure:\n\n

    * Structure of the project.

    ## Project description\n\n

    * This project is a ... 

    ## Dependencies\n\n

    * Before you can start using or working with this project, make sure to install the following dependencies:

    ## How to Install \n\n

    * To get this project up and running, follow these steps:

    ## How to Use\n\n

    * Once you have the project set up, you can start using it in the following ways:

    """
    print("\n\nfilename final" , filename)

    user_prompt = f"ignore structure that text context:\n\{content}, and create README.md"
    
    if(gpt_provider == "ollama"):
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        summary = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)

    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n\n**Error**: {summary['error']}\n\n"   
    formatted_summary = f"# Summary: {filename}\n\n{summary}"
    return formatted_summary

def summarize_with_ollama_LinkedIn_post(content, filename, gpt_provider, model):
    system_prompt = """
    You are a software engineer creating a LinkedIn post. 
    Summarize using knowledge you have from other open-source projects.
    Be direct in your responses; do not add comments.
    Format the response in Markdown, but not use ```Markdown```.
    """
    print("\n\nfilename final" , filename)

    user_prompt = f"ignore structure that text context:\n\{content}, and create a post for LinkedIn"
    
    if(gpt_provider == "ollama"):
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        summary = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)

    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n\n**Error**: {summary['error']}\n\n"   
    formatted_summary = f"# Summary: {filename}\n\n{summary}"
    return formatted_summary

import os

def get_project_files(directory):
    """
    Recursively gets all files in the provided directory, excluding paths that start with ".".
    """
    project_files = []
    for root, dirs, files in os.walk(directory):
        # Skip directories that start with "."
        dirs[:] = [d for d in dirs if not (d.startswith(".") or d.startswith("__"))]        
        
        for file in files:
            # Only add files with specific extensions and ignore those starting with "."
            if not file.startswith(".") and file.endswith(('.py', '.txt', '.html','.yml', '.js', '.ts', '.tsx', '.jsx', '.json')):
                project_files.append(os.path.join(root, file))
    return project_files


def read_and_summarize_file(filepath, gpt_provider, model, uploads_dir):
    """
    Reads a file and returns its summary using the specified model,
    saving the summary in the uploads directory with the same structure as the original file.
    """
    # start time
    start_time = time.time()
    filename = os.path.basename(filepath) 
    
    # Determine the relative path within the directory structure and create it in uploads
    os.makedirs(os.path.dirname(uploads_dir), exist_ok=True)
    
    # Read file content based on the file type
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
    
    # Generate the summary using the specified model
    summary = summarize_with_ollama_agent01(content, filename, gpt_provider, model)
    summary = summarize_with_ollama_agent02(summary, gpt_provider, model)
    # Save the summary to the uploads directory
    summary_filename = os.path.splitext(filename)[0] + "_summary.txt"
    summary_save_path = os.path.join(uploads_dir, summary_filename)

    with open(summary_save_path, 'w') as summary_file:
        summary_file.write(summary)

    # delay time
    end_time = time.time()
    print("\n\nTime taken to generate summary: ", end_time - start_time, "seconds\n\n")
    return summary  # Optionally return the summary if needed elsewhere
    

def generate_documentation(project_path, gpt_provider,  model, uploads_dir):
    """
    Generates documentation by summarizing each file in the project directory with the selected model,
    ignoring files that match any pattern in ignore_files.
    """
    documentation = []
    project_files = get_project_files(project_path)
    
    # Patterns to ignore
    ignore_patterns = ["project_documentation.txt"]
    
    for file_path in project_files:
        file_name = os.path.basename(file_path)
        
        # Skip files that match any pattern in ignore_patterns
        if any(fnmatch.fnmatch(file_name, pattern) for pattern in ignore_patterns):
            continue

        summary = read_and_summarize_file(file_path, gpt_provider , model, uploads_dir)
        # add delay between summaries 1 second
        documentation.append(summary)
        time.sleep(4)
    
    return "\n".join(documentation)
