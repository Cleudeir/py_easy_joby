import os
import time
import shutil
import tempfile
from flask import Blueprint,  render_template, request, Response, send_file, current_app
from src.Libs.Utils import normalize_path_name
from src.Libs.encrypt import encrypt_folder
from src.Libs.File_processor import (
    read_pdf, read_docx, split_file_by_regex,
    split_file_by_text, split_file_by_lines, split_file_by_paragraphs
)

file_splitter_routes = Blueprint('file_splitter_routes', __name__, template_folder='.')
output_folder = "src/.outputs"


def get_directory_output(request):
    user_ip = normalize_path_name(request.remote_addr)
    split_method = request.form['split_method']
    file_name = normalize_path_name(request.files['file'].filename)
    relative_output_folder = os.path.join(user_ip, split_method,  file_name)
    relative_output_folder_encrypt = encrypt_folder(relative_output_folder)
    absolute_output_folder = os.path.join(current_app.root_path, output_folder, relative_output_folder_encrypt)
    return absolute_output_folder , relative_output_folder_encrypt
    
@file_splitter_routes.route('/file-splitter', methods=['GET', 'POST'])
def file_splitter():
     # This will get the user's IP address
    
    if(request.method == 'GET'):
        return render_template('split_file.html')
    if request.method == 'POST':
        absolute_output_folder , relative_output_folder_encrypt = get_directory_output(request)
        file = request.files['file']
        split_method = request.form['split_method']
        split_value = request.form.get('split_value', '')
        split_regex = request.form.get('split_regex', '')
        file_name = file.filename
        file_extension = os.path.splitext(file_name)[1]
        
        # Define the output directory
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

        # Split the file based on method
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
        
        def generate_summary():
            if file.filename == '':
                    yield "<p>No file uploaded</p>\n"
                    return 
            yield "<p>Starting documentation generation...</p>\n"                       
            delay = 0.010
            for i, section in enumerate(sections):  
                         
                time.sleep(delay)            
                yield f"""{section}_save_/download_file/{relative_output_folder_encrypt}/{i+1}.txt"""        
        return Response(generate_summary(), mimetype="text/html")

@file_splitter_routes.route('/download_zip/<zip_folder>')
def download_zip(zip_folder):
    """ Dynamically generate and send a ZIP file for download """
    safe_folder = os.path.basename(zip_folder)
    directory = os.path.join(current_app.root_path, "src/.outputs", safe_folder)

    if not os.path.exists(directory):
        return "ZIP folder not found", 404

    # Create a temporary ZIP file
    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    zip_path = temp_zip.name

    # Zip the entire directory
    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', directory)

    return send_file(zip_path, as_attachment=True, download_name="split_files.zip")

@file_splitter_routes.route('/download_file/<path:file_path>')
def download_file(file_path):
    complete_path = os.path.join(current_app.root_path, output_folder, file_path)
    print(complete_path)
    if not os.path.exists(complete_path):
        return "File not found", 404
    return send_file(complete_path, as_attachment=True)
