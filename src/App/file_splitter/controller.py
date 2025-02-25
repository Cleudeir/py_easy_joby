import os
from flask import Blueprint, render_template, request, Response, send_file
from src.App.file_splitter.service import (
    download_zip_files, get_directory_output, process_file, generate_summary, create_zip, get_file_path
)

file_splitter_routes = Blueprint('file_splitter_routes', __name__, template_folder='.')

@file_splitter_routes.route('/file-splitter', methods=['GET', 'POST'])
def file_splitter():
    if request.method == 'GET':
        return render_template('view_split.html')

    if request.method == 'POST':
        absolute_output_folder = get_directory_output(request)
        file = request.files['file']
        split_method = request.form['split_method']
        split_value = request.form.get('split_value', '')
        split_regex = request.form.get('split_regex', '')

        sections = process_file(file, split_method, split_value, split_regex, absolute_output_folder)
        
        if isinstance(sections, tuple): 
            return sections

        return Response(generate_summary(file, sections), mimetype="text/html")


@file_splitter_routes.route('/file-splitter/download_all', methods=['POST'])
def download_zip():
    uploads_dir = get_directory_output(request)    
    return download_zip_files(uploads_dir)