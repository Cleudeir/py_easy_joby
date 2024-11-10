import os
import time
from src.modules.file_processor import read_pdf, read_docx
from src.modules.gpt import get_ollama_response, get_genai_response
import fnmatch
from flask import current_app


system_prompt = """
    "You are a helpful assistant who summarizes files. 
    Follow this structure, not create code:
    ## Purpose of the Code\n
    * Brief description of the code's purpose.
    ##  Business rule\n    
    * Summary of the business rule.
    ## List external libraries\n
    (if existe element) 
    * libraries named (little description).
    (else)
    * No libraries used.
    ## methods or functions\n
    * list all methods or functions with a brief description.
    Be direct in your responses; do not add comments. 
    """

def summarize_with_ollama_agent01(content, gpt_provider, model):    
 
    user_prompt = f"Please provide a concise summary of this content:\n{content}"
    
    # Use Ollama to generate the summary with the specified model
    if(gpt_provider == "ollama"):
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        summary = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)

    # Check if the response is a dictionary, which indicates an error
    if isinstance(summary, dict) and "error" in summary:
        return f"**Error**: {summary['error']}\n"
    # Return the formatted summary
    return summary


def summarize_with_ollama_agent02(content,  gpt_provider, model):
 
    user_prompt = f"{content}\nAnalyze if response follow structure and fix if not. remove all comments, not add comments"
    
    # Use Ollama to generate the summary with the specified model
    if(gpt_provider == "ollama"):
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        summary = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)

    # Check if the response is a dictionary, which indicates an error
    if isinstance(summary, dict) and "error" in summary:
        return f"**Error**: {summary['error']}\n"
    # Return the formatted summary
    return summary

def summarize_with_ollama_final(content, filename, gpt_provider, model):
    system_prompt = """
    You are a software engineer creating a README.md for GitHub. 
    Summarize using knowledge you have from other open-source projects. 
    Be direct in your responses; do not add comments. 
    Format the response in Markdown, but not use ```Markdown```. 

    Follow this structure README.md, not create code:  
    ## Project structure:\n
    * Structure of the project.
    ## Project description\n
    * This project is a ... 
    ## Dependencies\n
    * Before you can start using or working with this project, make sure to install the following dependencies:
    ## How to Install \n
    * To get this project up and running, follow these steps:
    ## How to Use\n
    * Once you have the project set up, you can start using it in the following ways:

    """

    user_prompt = f"ignore structure that text context:\n\{content}, and create README.md"
    
    if(gpt_provider == "ollama"):
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        summary = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)

    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n**Error**: {summary['error']}\n"   
    formatted_summary = f"# Summary: {filename}\n{summary}"
    return formatted_summary

def summarize_with_ollama_LinkedIn_post(content, filename, gpt_provider, model):
    system_prompt = """
    You are a software engineer creating a LinkedIn post. 
    Summarize using knowledge you have from other open-source projects.
    Be direct in your responses; do not add comments.
    Format the response in Markdown, but not use ```Markdown```.
    """

    user_prompt = f"ignore structure that text context:\n\{content}, and create a post for LinkedIn"
    
    if(gpt_provider == "ollama"):
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif(gpt_provider == "gemini"):
        summary = get_genai_response(system_prompt=system_prompt, user_prompt=user_prompt)

    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n**Error**: {summary['error']}\n"   
    formatted_summary = f"# Summary: {filename}\n{summary}"
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
    try:
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
        summary = summarize_with_ollama_agent01(content, gpt_provider, model)
        summary = summarize_with_ollama_agent02(summary, gpt_provider, model)
        summary = f"## Summary: {filename}\n---\n{summary}\n---\n"
  
        # Save the summary to the uploads directory 
    
        split_path = uploads_dir.split('/')[-1]
        join_path = uploads_dir + filepath.split(split_path)[1]
        file_name_only = (join_path.split('/')[-1]).split('.')[0]
        join_path = '/'.join(join_path.split('/')[:-1]) + '/' + file_name_only + '.txt'

        print('summary_save_path --------------\n',join_path)
        os.makedirs(os.path.dirname(join_path), exist_ok=True)

        with open(join_path, 'w') as summary_file:
            summary_file.write(summary)

        # delay time around
        end_time = time.time()
        print("\nTime taken to generate summary: ", int((end_time - start_time) * 1000), "ms\n")


        return summary  # Optionally return the summary if needed elsewhere
    except Exception as e:
        return {"error": str(e)}
    

def generate_documentation(project_path, gpt_provider, model, uploads_dir):
    """
    Streams documentation summaries by processing each file in the project directory 
    with the selected model, ignoring files that match any pattern in ignore_files.
    """
    project_files = get_project_files(project_path)
    ignore_patterns = ["project_documentation.txt"]

    for file_path in project_files:
        file_name = os.path.basename(file_path)        
        # Skip files that match any pattern in ignore_patterns
        if any(fnmatch.fnmatch(file_name, pattern) for pattern in ignore_patterns):
            continue

        summary = read_and_summarize_file(file_path, gpt_provider, model, uploads_dir)
        
        # Yield each summary immediately after processing the file
        yield summary + "\n"
        
        # Add delay between summaries to avoid rate-limiting issues
        if(gpt_provider == "gemini"):
            time.sleep(4)
