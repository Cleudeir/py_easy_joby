import os
from flask import Blueprint, render_template, request, Response, send_file
from src.App.file_splitter.service import (
    get_directory_output, process_file, generate_summary, create_zip, get_file_path
)

file_splitter_routes = Blueprint('file_splitter_routes', __name__, template_folder='.')

@file_splitter_routes.route('/file-splitter', methods=['GET', 'POST'])
def file_splitter():
    if request.method == 'GET':
        return render_template('view_split.html')

    if request.method == 'POST':
        absolute_output_folder, relative_output_folder_encrypt = get_directory_output(request)
        file = request.files['file']
        split_method = request.form['split_method']
        split_value = request.form.get('split_value', '')
        split_regex = request.form.get('split_regex', '')

        sections = process_file(file, split_method, split_value, split_regex, absolute_output_folder)
        
        if isinstance(sections, tuple):  # Error handling
            return sections  

        return Response(generate_summary(file, sections, relative_output_folder_encrypt), mimetype="text/html")


@file_splitter_routes.route('/download_zip/<zip_folder>')
def download_zip(zip_folder):
    """Generates and sends a ZIP file"""
    zip_path = create_zip(zip_folder)
    if not zip_path:
        return "ZIP folder not found", 404
    return send_file(zip_path, as_attachment=True, download_name="split_files.zip")


@file_splitter_routes.route('/download_file/<path:file_path>')
def download_file(file_path):
    """Serves the requested file for download"""
    complete_path = get_file_path(file_path)
    if not complete_path or not os.path.exists(complete_path):
        return "File not found", 404
    return send_file(complete_path, as_attachment=True)
