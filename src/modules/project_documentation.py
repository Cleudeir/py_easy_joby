import os
import time
from src.modules.file_processor import read_pdf, read_docx
from src.modules.gpt import get_ollama_response, get_genai_response


def getGptSummary(system_prompt, user_prompt, gpt_provider, model):
    summary = None
    if gpt_provider == "ollama":
        summary = get_ollama_response(model, system_prompt, user_prompt)
    elif gpt_provider == "gemini":
        summary = get_genai_response(system_prompt, user_prompt)
    if isinstance(summary, dict) and "error" in summary:
        return f"**Error**: {summary['error']}\n"
    return f"""{summary}"""


def get_summary(content, filename, gpt_provider, model):
    system_prompt = """
    you are a software engineer creating a project documentation.  
    """
    initial_user_prompt = f"""
    This is a code:
    {content}
    Structure:
    """
    finally_user_prompt = f"""
    create follow this structure.
    """
    user_prompt = f"""
    {initial_user_prompt}    
    # {filename}
    ##  Project purpose and description
        * ...
    {finally_user_prompt}
    """
    summary = getGptSummary(system_prompt, user_prompt, gpt_provider, model)
    time.sleep(4)
    # ----------------------------------------------------------------------
    user_prompt = f"""
    {initial_user_prompt}
    ## Execute Flow 
        * ...
    {finally_user_prompt}
    """
    summary += getGptSummary(system_prompt, user_prompt, gpt_provider, model)
    time.sleep(4)
    # ----------------------------------------------------------------------
    user_prompt = f"""
    {initial_user_prompt}
    ## External libs
        * ...
    {finally_user_prompt}
    """
    summary += getGptSummary(system_prompt, user_prompt, gpt_provider, model)
    time.sleep(4)
    return summary


def get_generic_summary(summary, gpt_provider, model):
    system_prompt = """
    You are a software engineer creating a README.md to document a project.
    """
    initial_user_prompt = f"""
    That is summary:
    {summary}
    Follow this structure to create a summary:
    """
    finally_user_prompt = f"""
    Create general summary of this project, no comments, no explanation, responda em Portuguese.
    Create summary without create code.
    """
    # ----------------------------------------------------------------------
    user_prompt = f"""  
    {initial_user_prompt}
    ## Project purpose and description
        * ...
    {finally_user_prompt}
    """

    _summary = getGptSummary(system_prompt, user_prompt, gpt_provider, model)
    time.sleep(4)
    # ----------------------------------------------------------------------
    user_prompt = f"""
    {initial_user_prompt}
    ## How to Install
        * To get this project up and running, follow these steps:
        * **Clone this repository;
        * **Install dependencies:** `...`;
        * **Create a .env file:** `...`;
        * **Run the application:** `...`;      
    {finally_user_prompt}
    """
    _summary += getGptSummary(system_prompt, user_prompt, gpt_provider, model)
    time.sleep(4)
    # ----------------------------------------------------------------------
    user_prompt = f"""
    {initial_user_prompt}
    ## Dependencies
    * Before you can start using or working with this project, make sure to install the following dependencies:
        ```
        * Dependencies name - whats this does?
        ```
    Create general summary of this project, no comments, no explanation, responda em Portuguese.
    Create summary without create code.
    """
    # ----------------------------------------------------------------------
    user_prompt = f"""
    That is summary:
    {summary}
    Follow this structure to create a summary:
    ## how is architecture and design
        *  ...
    {finally_user_prompt}
    """
    _summary += getGptSummary(system_prompt, user_prompt, gpt_provider, model)
    time.sleep(4)
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


def read_and_summarize_file(filepath, gpt_provider, model, uploads_dir, useCache):
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
        if useCache:
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
