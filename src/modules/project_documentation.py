import os
import time
from src.modules.file_processor import read_pdf, read_docx
from src.modules.gpt import get_ollama_response, get_genai_response
from flask import current_app


def get_summary(content, filename, gpt_provider, model):
    system_prompt = """
    you are a software engineer creating a project documentation.  
    """

    user_prompt = f"""
    This is a code:
    {content}
    Flow structure and summary, no comments, no explanation:
    ## Summary: 
        * {filename}
    ##  Project purpose and description
        * ...        
    ## how is Pipeline
        * ...
    ## Input
        ### Internal dependencies           
            * Name modules           
        ### External dependencies           
            * Name libraries            
    ## Output
        * ...
    ---
    """

    # Use Ollama to generate the summary with the specified model
    if gpt_provider == "ollama":
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif gpt_provider == "gemini":
        summary = get_genai_response(
            system_prompt=system_prompt, user_prompt=user_prompt
        )
    # Check if the response is a dictionary, which indicates an error
    if isinstance(summary, dict) and "error" in summary:
        return f"**Error**: {summary['error']}\n"
    # Return the formatted summary
    return summary


def get_general_summary(summary, gpt_provider, model):
    system_prompt = """
    You are a software engineer creating a README.md for GitHub.
    """
    user_prompt = f"""
    That is summary:
    {summary}
    Follow this structure:
    ## Project purpose and description
        * ... 
    ## Dependencies
        * Before you can start using or working with this project, make sure to install the following dependencies:
        ```
        * Dependencies name
        ``
    ## How to Install
        * To get this project up and running, follow these steps:
            * **Clone this repository;
            * **Install dependencies:** `...`;
            * **Create a .env file:** `...`;
            * **Run the application:** `...`;            
    ## How to Use
        *  ...
    ## how is architecture
        *  ...
    ## how is pipeline
        *  ...
    
    Create general summary of this project, not create code, no comments, no explanation, responda em Portuguese.
    """

    if gpt_provider == "ollama":
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif gpt_provider == "gemini":
        summary = get_genai_response(
            system_prompt=system_prompt, user_prompt=user_prompt
        )

    if isinstance(summary, dict) and "error" in summary:
        return f"**Error**: {summary['error']}\n"

    return summary


def get_linkedIn_post(summary, general_summary, filename, gpt_provider, model):
    system_prompt = """
    You are a software engineer creating a post for LinkedIn.
    """

    user_prompt = f"that is summary project:{general_summary}, and create a post for LinkedIn, responda em Portuguese."

    if gpt_provider == "ollama":
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif gpt_provider == "gemini":
        summary = get_genai_response(
            system_prompt=system_prompt, user_prompt=user_prompt
        )

    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n**Error**: {summary['error']}\n"
    formatted_summary = f"# Summary: {filename}\n{summary}"
    return formatted_summary


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
                (".py", ".txt", ".html", ".yml", ".js", ".ts", ".tsx", ".jsx", ".json")
            ):
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

        split_path = uploads_dir.split("/")[-1]
        join_path = uploads_dir + filepath.split(split_path)[1]
        file_name_only = (join_path.split("/")[-1]).split(".")[0]
        join_path = "/".join(join_path.split("/")[:-1]) + "/" + file_name_only + ".txt"

        # check if file already exists
        if os.path.exists(join_path):
            # read file and return
            with open(join_path, "r") as file:
                return file.read()

        # Determine the relative path within the directory structure and create it in uploads
        os.makedirs(os.path.dirname(uploads_dir), exist_ok=True)

        # Read file content based on the file type
        content = None
        if filepath.endswith(".txt"):
            with open(filepath, "r") as file:
                content = file.read()
        elif filepath.endswith(".pdf"):
            with open(filepath, "rb") as file:
                content = read_pdf(file)
        elif filepath.endswith(".docx"):
            with open(filepath, "rb") as file:
                content = read_docx(file)
        else:
            with open(filepath, "r") as file:
                content = file.read()

        if gpt_provider == "gemini":
            time.sleep(4)

        # Generate the summary using the specified model
        summary = get_summary(content, filename, gpt_provider, model)
        # Save the summary to the uploads directory

        os.makedirs(os.path.dirname(join_path), exist_ok=True)
        with open(join_path, "w") as summary_file:
            summary_file.write(summary)

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
