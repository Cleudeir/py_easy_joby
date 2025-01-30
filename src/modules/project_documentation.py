import os
import time
from src.modules.file_processor import read_pdf, read_docx
from Libs.LLM.Provider import get_ollama_text, get_genai_text
from src.Libs.Files import (create_folder_by_file_path, read_file_binary_content,
    read_file_content, save_content_to_file)


def getGptSummary(system_prompt, user_prompt, gpt_provider):
    summary = None
    if gpt_provider == "ollama":
        summary = get_ollama_text(system_prompt, user_prompt)
    elif gpt_provider == "gemini":
        summary = get_genai_text(system_prompt, user_prompt)
    if isinstance(summary, dict) and "error" in summary:
        return f"**Error**: {summary['error']}\n"
    return f"""{summary}"""


def get_summary(content, filename, gpt_provider):
    system_prompt = """
    you are a software engineer creating a project documentation.  
    """
    initial_user_prompt = f"""
    This is a code:
    {content}
    Structure:
    """    
    # ----------------------------------------------------------------------
    user_prompt = f"""
    {initial_user_prompt}    
    # {filename}
    ##  Project purpose and description
        * ...
    create follow this structure.
    """
    summary = getGptSummary(system_prompt, user_prompt, gpt_provider)   
    return summary


def get_generic_summary(summary, gpt_provider):
    system_prompt = """
    You are a software engineer creating a project summary.
    """
    initial_user_prompt = f"""
    That is summary:
    {summary}
    Follow this structure to create a summary:
    """
    finally_user_prompt = f"""
    Create general summary of this project, no comments, no explanation.
    Create summary without create code.
    """
    # ----------------------------------------------------------------------
    user_prompt = f"""  
    {initial_user_prompt}
    ## Summary
        ...(in details) 
    ## Tech Stack
        ...
    {finally_user_prompt}
    """
    _summary = getGptSummary(system_prompt, user_prompt, gpt_provider)
    # ----------------------------------------------------------------------   
    return _summary

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
            if not file.startswith(".") and file.endswith(
                (
                    ".py",
                    ".txt",
                    ".html",
                    ".yml",
                    ".js",
                    ".ts",
                    ".tsx",
                    ".jsx",
                    ".json",
                    "java",
                )
            ):
                project_files.append(os.path.join(root, file))
    return project_files


def read_and_summarize_file(filepath, gpt_provider, uploads_dir, useCache):
    try:
        """
        Reads a file and returns its summary using the specified model,
        saving the summary in the uploads directory with the same structure as the original file.
        """
        # start time
        start_time = time.time()
        filename = os.path.basename(filepath)

        split_path = uploads_dir.split("/")[-1]
        join_path = uploads_dir + filepath.split(split_path)[1]
        file_name_only = (join_path.split("/")[-1]).split(".")[0]
        join_path = "/".join(join_path.split("/")[:-1]) + "/" + file_name_only + ".txt"

        # check if file already exists      
        if os.path.exists(join_path) and useCache:
            read_file_content(join_path)             

        # Determine the relative path within the directory structure and create it in uploads
        create_folder_by_file_path(uploads_dir)

        # Read file content based on the file type
        content = None
        if filepath.endswith(".pdf"):
            binary = read_file_binary_content(filepath)     
            content = read_pdf(binary)
        elif filepath.endswith(".docx"):
            binary = read_file_binary_content(filepath)           
            content = read_docx(binary)
        else:
            content = read_file_content(filepath)          

        if gpt_provider == "gemini":
            time.sleep(4)

        # Generate the summary using the specified model
        summary = get_summary(content, filename, gpt_provider)
        # Save the summary to the uploads directory

        save_content_to_file(join_path, summary)
     
        # delay time around
        end_time = time.time()
        print(
            "\nTime taken to generate summary: ",
            int((end_time - start_time) * 1000),
            "ms\n",
        )
        return summary  # Optionally return the summary if needed elsewhere
    except Exception as e:
        return {"error": str(e)}
