from src.Libs.LLM.Provider import get_text
import os
import time
import markdown
from flask import current_app
from src.Libs.Files import read_file_content, save_content_to_file
from src.Libs.File_processor import read_docx, read_pdf
from src.Libs.Utils import normalize_path_name, time_format_string, extract_code_blocks, parseTextToWeb
from src.Libs.encrypt import encrypt_folder

output_folder = "src/.outputs"

def get_directory_output(request):
    """Generates an encrypted output directory based on request"""
    user_ip = normalize_path_name(request.remote_addr)
    project_name = normalize_path_name(request.form.get("project_name", ""))
    relative_output_folder = os.path.join(user_ip, project_name)
    relative_output_folder_encrypt = encrypt_folder(relative_output_folder)
    absolute_output_folder = os.path.join(current_app.root_path, output_folder, relative_output_folder_encrypt)
    return absolute_output_folder


def process_uploaded_files(files):
    """Processes uploaded files and extracts content"""
    list_content = []
    for file in files:
        file_name = file.filename
        try:
            binary_content = file.read()
            content = None
            if file_name.endswith(".pdf"):
                content = read_pdf(binary_content)
            elif file_name.endswith(".doc"):
                content = read_docx(binary_content)
            elif file_name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                continue  # Skip image files
            else:
                content = binary_content.decode('utf-8')

            list_content.append({
                "file_name": file_name,
                "content": content
            })
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
    
    return list_content


def generate_summary(files, list_content, uploads_dir, use_cache):
    """Generates documentation summary for uploaded files"""
    if not files or all(file.filename == '' for file in files):
        yield "<p>No files uploaded.</p>\n"
        return

    combined_summary = ""
    yield "<p>Starting documentation generation...</p>\n"
    delay = 0.010

    for content in list_content:
        start_time = time.time()
        file_name = content["file_name"]
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

        # Generate code based on summary
        start_time = time.time()
        gen_code = None
        if os.path.exists(file_path) and use_cache:
            time.sleep(delay)
            gen_code = read_file_content(file_path)
        else:
            gen_code = get_generate_code(file_name, summary)
            save_content_to_file(file_path, extract_code_blocks(gen_code))

        elapsed_time = time_format_string(start_time)
        file_code = f"<pre><code id='agent_coder'>{parseTextToWeb(extract_code_blocks(gen_code))}</code></pre>\n"
        yield markdown.markdown(f"<p>Creating code for : <strong>{file_name}</strong></p>")
        yield markdown.markdown(f"{file_code}\n<p>Time render: <strong>{elapsed_time}</strong></p>\n")

    # Generate final project summary
    start_time_final = time.time()
    final_summary = get_final_summary(summary=combined_summary)
    time.sleep(delay)
    elapsed_time_final = time_format_string(start_time_final)

    yield markdown.markdown(f"<p>Creating summary for : <strong>README.md</strong></p>")
    yield markdown.markdown(f"{final_summary}\n<p>Time render: <strong>{elapsed_time_final}</strong></p>\n")

    save_content_to_file(os.path.join(uploads_dir, "README.md"), final_summary)
    yield "<p>Summary generation complete</p>\n"



def get_summary(content):
    system_prompt = """
    you are a software engineer create documentation explain to the user.  
    """ 
    # ----------------------------------------------------------------------
    user_prompt = f"""
    This is a file, you need summary:
    {content}
    Create this one-paragraph summary using layman's terms and non-technical. no use of code, creation of summary, no comments, no suggestions, no corrections, no explanation.
    Follow this structure markdown:  
    ## Summary
        ...(once paragraph)
    """
    summary = get_text(system_prompt, user_prompt)   
    return summary

def get_generate_code(file_name, summary):
    system_prompt = """
    you are a software engineer.  
    """ 
    # ----------------------------------------------------------------------
    user_prompt = f"""
    That is summary the code:
    {summary}
    create code for file:{file_name}
        -use best practices, 
        -complete with all function and logics
        -no use of code
        -no comments
        -no explanation.
        -using perfect indentation     
    """
    code = get_text(system_prompt, user_prompt)
    # ----------------------------------------------------------------------   
    return code

def get_final_summary(summary):
    system_prompt = """
    you are a software engineer create documentation explain to the user. use all time to elaborate best summary.
    """
    # ----------------------------------------------------------------------
    user_prompt = f"""  
    That is summary:
    {summary}
    Create a three-paragraph summary using this summary code files, create a summary explain this code base works, your business rules. no use code, no comments, no explanation.
    Follow this structure to create a summary:
    ## Summary
        ...(in details)
    ## Business Rules
        ...(bullet points)   
    ## Tech Stack 
        ...(bullet points)
    """
    _summary = get_text(system_prompt, user_prompt)
    # ----------------------------------------------------------------------   
    return _summary