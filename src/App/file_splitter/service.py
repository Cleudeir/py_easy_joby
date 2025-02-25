import io
import os
import time
import zipfile
from flask import current_app, send_file
from src.Libs.Utils import normalize_path_name
from src.Libs.encrypt import encrypt_folder
from src.Libs.File_processor import (
    read_pdf, read_docx, split_file_by_regex,
    split_file_by_text, split_file_by_lines, split_file_by_paragraphs
)

output_folder = "src/.outputs"

def get_directory_output(request):
    print('get_directory_output')
    user_ip = normalize_path_name(request.remote_addr)
    split_method = request.form['split_method']
    file_name = normalize_path_name(request.files['file'].filename)
    module_name = "file_splitter"
    print(file_name, split_method, user_ip, module_name)
    relative_output_folder = os.path.join(user_ip, split_method, file_name)
    relative_output_folder_encrypt = encrypt_folder(relative_output_folder)
    absolute_output_folder = os.path.join(current_app.root_path, output_folder, relative_output_folder_encrypt)
    return absolute_output_folder



def create_zip(directory):
    print('create_zip', directory)
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
    file_zip_name = uploads_dir.split("/")[-1]
    return send_file(zip_buffer, mimetype="application/zip", as_attachment=True, download_name=f"{file_zip_name}.zip")

def process_file(file, split_method, split_value, split_regex, absolute_output_folder):
    """Processes the uploaded file and splits it based on the selected method"""
    file_name = file.filename
    file_extension = os.path.splitext(file_name)[1]

    binary_content = file.read()
    file_content = None

    if file_extension == ".pdf":
        file_content = read_pdf(binary_content)
    elif file_extension in [".doc", ".docx"]:
        file_content = read_docx(binary_content)
    elif file_extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
        return "Unsupported file type", 400
    else:
        try:
            file_content = binary_content.decode('utf-8')
        except UnicodeDecodeError:
            return "Unable to process file encoding.", 400

    # Splitting Logic
    sections = []
    if split_method == 'text':
        if not split_value:
            return "Please provide text to split by.", 400
        sections = split_file_by_text(file_content, split_value, absolute_output_folder)
    elif split_method == 'regex':
        if not split_regex:
            return "Please provide regex pattern to split by.", 400
        sections = split_file_by_regex(file_content, split_regex, absolute_output_folder)
    elif split_method == 'lines':
        if not split_value.isdigit():
            return "Please provide a valid number of lines to split by.", 400
        sections = split_file_by_lines(file_content, int(split_value))
    elif split_method == 'paragraphs':
        sections = split_file_by_paragraphs(file_content)
    else:
        return "Invalid split method", 400

    return sections


def generate_summary(file, sections):
    """Generates streaming summary response"""
    if file.filename == '':
        yield "<p>No file uploaded</p>\n"
        return 
    yield "<p>Starting documentation generation...</p>\n"                       
    delay = 0.010
    if(len(sections) == 0):
        time.sleep(delay) 
        yield "<p>Not found any section</p>\n"
        return
    for i, section in enumerate(sections):  
        time.sleep(delay)            
        yield f"""{section}"""  

def get_file_path(file_path):
    """Returns the complete file path"""
    return os.path.join(current_app.root_path, output_folder, file_path)
