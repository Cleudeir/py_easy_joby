import base64
import os
import time
import markdown
import zipfile
import io
from flask import current_app, send_file
from src.Libs.LLM.Provider import get_text, get_vision
from src.Libs.File_processor import read_file_content, save_content_to_file
from src.Libs.File_processor import read_docx, read_pdf
from src.Libs.Utils import normalize_path_name, time_format_string
from src.Libs.encrypt import encrypt_folder

def get_directory_output(request):
    """Generates an encrypted output directory based on request"""
    user_ip = normalize_path_name(request.remote_addr)
    print(user_ip)
    files = request.files.getlist('project_path')
    module_name = "project_documentation"
    project_name = ""
    for file in files:
        full_path = file.filename
        # start with
        project_name = normalize_path_name(full_path.split("/")[0])
        break
    relative_output_folder = os.path.join(user_ip, project_name, module_name)
    relative_output_folder_encrypt = encrypt_folder(relative_output_folder)
    
    output_folder = "src/.outputs"  
    absolute_output_folder = os.path.join(current_app.root_path, output_folder, relative_output_folder_encrypt)
    return absolute_output_folder

def create_zip(directory):
    """Creates an in-memory ZIP file from the given directory."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zipf.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer

def download_zip_files(uploads_dir):    
    zip_buffer = create_zip(uploads_dir)
    print("uploads_dir", uploads_dir)
    file_zip_name = uploads_dir.split("/")[-1]
    return send_file(zip_buffer, mimetype="application/zip", as_attachment=True, download_name=f"{file_zip_name}.zip")

def process_uploaded_files(files, read_images=True):
    """Processes uploaded files and extracts content"""
    list_content = []
    for file in files:
        full_path = file.filename
        print(full_path)
        # start with
        paths = full_path.split("/")
        checkFile = False
        for path in paths:        
            exclusions = [            # Files that start with a dot
                "__pycache__",        # Python bytecode cache folder
                ".git",               # Git directory
                ".svn",               # Subversion directory
                ".idea",              # IDE project folder (e.g., PyCharm)
                "node_modules",       # Node.js modules directory
                "dist",               # Build directory for many languages
                "build",              # Build directory
                ".vscode",            # Visual Studio Code settings
                ".DS_Store",          # macOS-specific file
                "README.md",          # README file
                ]
            if any(exclusion in path for exclusion in exclusions) or path.startswith("."):
                checkFile = True
        if checkFile:
            continue
        try:
            binary_content = file.read()
            content = None
            if full_path.endswith(".pdf"):
                content = read_pdf(binary_content)
            elif full_path.endswith(".doc"):
                content = read_docx(binary_content)
            elif read_images and full_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                binary_content
                content = base64.b64encode(binary_content).decode('utf-8')
            else:
                content = binary_content.decode('utf-8')

            list_content.append({
                "file_name": full_path,
                "content": content
            })
        except Exception as e:
            print(f"Error reading file {full_path}: {e}")
            continue
    
    return list_content


def generate_summary(files, list_content, uploads_dir, use_cache, read_images):
    """Generates documentation summary for uploaded files"""
    if not files or all(file.filename == '' for file in files):
        yield "<p>No files uploaded.</p>\n"
        return

    combined_summary = ""
    yield "<p>Starting documentation generation...</p>\n"
    delay = 0.1

    if(len(list_content) == 0):
        time.sleep(delay) 
        yield "<p>Not found files</p>\n"
        return

    for content in list_content:
        start_time = time.time()
        file_name = content["file_name"]
        print(file_name)
        if file_name == '':
            yield "<p>File name is empty</p>\n"
            break

        file_path = os.path.join(uploads_dir, file_name)
        summary_path = file_path + ".md"

        # Check cache or generate summary
        if os.path.exists(summary_path) and use_cache:
            time.sleep(delay)
            summary = read_file_content(summary_path)
        else:
            summary = get_summary(content)
            save_content_to_file(summary_path, summary)

        combined_summary += f"## {file_name}\n\n{summary}\n\n"
        yield markdown.markdown(f"<p>Creating summary for : <strong>{file_name}</strong></p>")
        elapsed_time = time_format_string(start_time)
        yield markdown.markdown(f"{summary}\n<p>Time render: <strong>{elapsed_time}</strong></p>\n")

    # Generate final project summary
    time.sleep(delay)
    yield markdown.markdown(f"<p>Creating summary: <strong>README.md</strong></p>")
    time.sleep(delay)
    final_summary = get_final_summary(summary=combined_summary)
    check1 = get_final_summary_check(readme=final_summary)
    check2 = get_final_summary_check(readme=final_summary)
    while not ("This README follows the structure" in check1 and "This README follows the structure" in check2):
        final_summary = get_final_summary(summary=combined_summary)
        check1 = get_final_summary_check(readme=final_summary)
        check2 = get_final_summary_check(readme=final_summary)
    
    yield markdown.markdown(f"{final_summary}\n<p>Time render: <strong>{time_format_string(start_time)}</strong></p>\n")

  
    readme_path = os.path.join(uploads_dir, "README.md")
    save_content_to_file(readme_path, final_summary)
    
    time.sleep(delay)
    yield "<p>Summary generation complete</p>\n"
        



def get_summary(content):
    print('get_summary',content.get("content"))
    system_prompt = """
You are a software engineer. Your task is to create documentation that explains things to the user in simple terms.
""" 
# ----------------------------------------------------------------------

    summary = ""
    if(content.get("file_name").lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))):
        user_prompt = f"""
Read the image. You need to create a summary:
Write a one-paragraph summary in layman's terms and avoid using any technical language. Do not use code, provide explanations, suggestions, or corrections.
Follow this structure in markdown:

## Summary

    ...(one paragraph summary)
        """
        summary = get_vision(system_prompt, user_prompt, content.get("content"))
    else:
        user_prompt = f"""
This is a file. You need to create a summary:
{content.get("content")}
Write a one-paragraph summary in layman's terms and avoid using any technical language. Do not use code, provide explanations, suggestions, or corrections.

Follow this structure in markdown:
## Summary

...(one paragraph summary)
        """
        summary = get_text(system_prompt, user_prompt)   
    return summary

def get_final_summary(summary):
    system_prompt = """
    you are a software engineer create documentation explain to the user. use all time to elaborate best summary.
    """
    # ----------------------------------------------------------------------
    user_prompt = f"""  
    That is  summary:
    {summary}
    This is the union of all summaries of the project files. you need create a general summary, follow this structure:
----------------------------------------
## Summary
    (Summary project do in details)
## Project do
    (bullet points)   
## Tech Stack 
    (bullet points)
----------------------------------------
note : response in English, avoid using code, comments, or explanations in the response.
    """
    _summary = get_text(system_prompt, user_prompt)
    # ----------------------------------------------------------------------   
    return _summary


def get_final_summary_check(readme):
    system_prompt = """
    you are a software engineer create documentation explain to the user. use all time to elaborate best summary.
    """
    # ----------------------------------------------------------------------
    user_prompt = f"""
You are tasked with verifying whether a README file strictly follows a predefined structure. The structure you need to check is as follows:

## Summary
    - A detailed explanation of the project.

## Project do
    - A list of tasks, objectives, and requirements for the project. This should be presented in bullet points.
    
## Tech Stack
    - A list of technologies, frameworks, libraries, and tools used in the project. This should be presented in bullet points.

**Validation Criteria:**
0. Check response in English.
1. The README **must** contain all three sections: `Summary`, `Business Rules`, and `Tech Stack`, in the exact order.
2. Each section **must** contain relevant content:
   - `Summary`: A descriptive explanation of the project.
   - `Project do`: Clearly in bullet points.
   - `Tech Stack`: A bullet-point list of technologies used.
3. The README **must not** contain any additional sections, headers, or unrelated content beyond what is specified above.

**Your Task:**
- If the README **strictly** follows the above structure and contains only the specified sections, respond with:
  - `"This README follows the structure"`
- If the README is missing any required section, contains incorrect formatting, or includes additional information beyond the specified structure, respond with:
  - `"This README does not follow the structure"`
  
** Automatic reproved:**
- no response in English
Here is the README content you need to evaluate:
----------------------------------------
{readme}
----------------------------------------

Note: No comments, suggestions, corrections, or explanations are required. Just the response confirming whether the README follows the structure or not.
"""

    _summary = get_text(system_prompt, user_prompt)
    # ----------------------------------------------------------------------   
    return _summary