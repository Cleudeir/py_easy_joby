import os
import zipfile
import shutil
import tempfile
from flask import Blueprint, current_app, render_template, request, send_file, send_from_directory, abort, url_for, redirect
from src.Libs.File_processor import (
    read_pdf, read_docx, read_txt, split_file_by_regex,
    split_file_by_text, split_file_by_lines, split_file_by_paragraphs
)

file_splitter_routes = Blueprint('file_splitter_routes', __name__, template_folder='.')

@file_splitter_routes.route('/file-splitter', methods=['GET', 'POST'])
def file_splitter():
    if request.method == 'POST':
        file = request.files['file']
        split_method = request.form['split_method']
        split_value = request.form.get('split_value', '')
        split_regex = request.form.get('split_regex', '')
        file_name = file.filename
        file_extension = os.path.splitext(file_name)[1]
        
        # Define the output directory
        output_folder = file_name.replace(" ", "_").replace(".", "_")
        uploads_dir = os.path.join(current_app.root_path, "src/.outputs", output_folder, split_method)
        print(uploads_dir)
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
            sections = split_file_by_text(file_content, split_value, uploads_dir)
        elif split_method == 'regex':
            if not split_regex:
                return "Please provide regex pattern to split by.", 400
            sections = split_file_by_regex(file_content, split_regex, uploads_dir)
        elif split_method == 'lines':
            if not split_value.isdigit():
                return "Please provide a valid number of lines to split by.", 400
            sections = split_file_by_lines(file_content, int(split_value))
        elif split_method == 'paragraphs':
            sections = split_file_by_paragraphs(file_content)
        else:
            return "Invalid split method", 400
        
        files = []

        for i, section in enumerate(sections):
            files.append(f"{i+1}.txt:\n{section}")

        return render_template(
            'split_results.html',
            sections=files,
            split_method=split_method,
            zip_folder=output_folder
        )

    return render_template('split_file.html')


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


@file_splitter_routes.route('/download_file/<zip_folder>/<split_method>/<file_name>')
def download_file(zip_folder,split_method, file_name):
    """ Serve individual split files for download """
    safe_folder = os.path.basename(zip_folder)
    directory = os.path.join(current_app.root_path, "src/.outputs", safe_folder, split_method)
    file = os.path.join(directory, file_name)
    print(file)
    if not os.path.exists(file):
        abort(404)

    return send_from_directory(directory, file_name, as_attachment=True)
