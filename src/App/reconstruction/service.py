
import os
import markdown
import time
from flask import current_app
from src.Libs.Utils import extract_code_blocks, normalize_path_name
from src.Libs.encrypt import encrypt_folder
from src.Libs.LLM.Provider import  get_text
from src.Libs.File_processor import save_content_to_file

def generate_documentation(filename, file_content, output_path):
    yield "<p>Starting documentation generation...</p>\n"
    delay = 0.5
    time.sleep(delay)
    yield "<p>Original code</p>\n"
    time.sleep(delay)
    yield markdown.markdown(f"<pre><code id='agent_coder'>{replaceCodeArrow(code=file_content)}</code></pre>")
    time.sleep(delay)
    summary = get_agent_summary(file_content)
    yield markdown.markdown(summary)
    code = get_agent_coder(summary)
    yield f"<pre><code id='agent_coder'>{replaceCodeArrow(code)}</code></pre>"             
    # Save file
    file_resume = os.path.join(output_path, filename + '.md')                             
    save_content_to_file(file_resume, summary)            
    # Save files
    file_code_reconstruction = os.path.join(output_path, filename)                
    save_content_to_file(file_code_reconstruction, code)
    time.sleep(delay)
    yield "<p>Summary generation complete</p>\n"
    return
                
def replaceCodeArrow(code):
    if("<" in code):
        return code.replace('<', '&lt;')
    return code

def get_directory_output(request):
    """Generates an encrypted output directory based on request"""
    user_ip = normalize_path_name(request.remote_addr)
    print(user_ip)
    file_name = normalize_path_name(request.files['file'].filename)
    module_name = "reconstruction"
    relative_output_folder = os.path.join(user_ip, file_name, module_name)
    relative_output_folder_encrypt = encrypt_folder(relative_output_folder)
    
    output_folder = "src/.outputs"
    
    absolute_output_folder = os.path.join(current_app.root_path, output_folder, relative_output_folder_encrypt)
    return absolute_output_folder

def get_agent_summary(file_content):    
    system_prompt  = "You are a software engineer. will create documentation."     

    user_prompt = f"""
This is a file. You need to create a summary:
{file_content}   
Write a summary in layman's terms and avoid using any technical language. Do not use code, provide explanations, suggestions, or corrections.

Follow this structure in markdown:
## Summary
    ...(teen paragraph summary) 
    """
    # Use Ollama to generate the summary with the specified model
    data = get_text(system_prompt, user_prompt)
    return data

def get_agent_coder(summary):   
    system_prompt  = "You are a software engineer will create a code"
    summary = f"""
Create a code based in this summary:

{summary}

Rules to follow:

Do not include comments in the code.
Do not provide any explanations.
Ensure perfect indentation throughout.
Provide a complete code solution.
    """
    # Use Ollama to generate the summary with the specified model
    data = get_text( system_prompt, summary)  
    return extract_code_blocks(data)
