import fnmatch
import os
import time
from Libs.File_processor import read_pdf, read_docx
from src.Libs.LLM.Provider import get_ollama_text, get_genai_text
from src.Libs.Files import (create_folder_by_file_path, read_file_binary_content,
    read_file_content, save_content_to_file)
from src.Libs.LLM.Provider import get_text



def get_summary(content, filename):
    system_prompt = """
    you are a software engineer creating a project documentation.  
    """ 
    # ----------------------------------------------------------------------
    user_prompt = f"""
    This is a code:
    {content}
    Structure:
    # {filename}
    ##  Project purpose and description
        * ...
    create follow this structure.
    """
    summary = get_text(system_prompt, user_prompt)   
    return summary


def get_final_summary(summary):
    system_prompt = """
    You are a software engineer creating a project summary.
    """
    # ----------------------------------------------------------------------
    user_prompt = f"""  
    That is summary:
    {summary}
    Follow this structure to create a summary:
    ## Summary
        ...(in details) 
    ## Tech Stack 
        ...(bullet points)
    Create general summary of this project, no comments, no explanation.
    Create summary without create code.
    """
    _summary = get_text(system_prompt, user_prompt)
    # ----------------------------------------------------------------------   
    return _summary

def get_project_files(files):
    project_files = []
    ignore_patterns = ["project_documentation.txt", "readme.txt"]
    
    for file in files:     
        try:
            file_name = file.filename
            print(file_name)

            if any(fnmatch.fnmatch(file_name, pattern) for pattern in ignore_patterns):                
                continue

            if not file_name.startswith(".") and file_name.endswith((
                ".py", ".txt", ".html", ".yml", ".js", ".ts", ".tsx", ".jsx", ".json", ".java"
            )):
                # Read file content
                binary_content = file.read()  # Read the file content once
                print(f"File content read: {len(binary_content)}")
                # file.seek(0)  # Reset file pointer for Flask to reuse if needed
                # print(f"File content read: {binary_content}")

                # content = None
                # if file_name.endswith(".pdf"):
                #     content = read_pdf(binary_content)  # Use binary_content directly
                # elif file_name.endswith(".docx"):
                #     content = read_docx(binary_content)  # Use binary_content directly
                # else:
                #     content = binary_content.decode('utf-8')  # Decode for text-based files

                # if content is not None:
                #     project_files.append({"name": file_name, "content": content})

        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
            continue  # Continue processing other files
    
    return project_files




def read_and_summarize_file(file, uploads_dir, useCache):
    try:
        """
        Reads a file and returns its summary using the specified model,
        saving the summary in the uploads directory with the same structure as the original file.
        """
        # start time
        start_time = time.time()

        content = file.get("content")
        filename = file.get("name")

        split_path = uploads_dir.split("/")[-1]
        join_path = uploads_dir + filename.split(split_path)[1]
        file_name_only = (join_path.split("/")[-1]).split(".")[0]
        join_path = "/".join(join_path.split("/")[:-1]) + "/" + file_name_only + ".txt"

        # check if file already exists      
        if os.path.exists(join_path) and useCache:
            read_file_content(join_path)             

        # Determine the relative path within the directory structure and create it in uploads
        create_folder_by_file_path(uploads_dir)

        # Read file content based on the file type
                

        # Generate the summary using the specified model
        summary = get_summary(content, filename)
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
