import os
from flask import Blueprint, current_app, render_template, request
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
        uploads_dir = os.path.join(current_app.root_path, "src/.outputs/" + file_name +"/"+ split_method + "/")
        # remove contents of uploads dir
        if os.path.exists(uploads_dir):
            for f in os.listdir(uploads_dir):
                os.remove(os.path.join(uploads_dir, f))
        else:
            os.makedirs(uploads_dir)
        binary_content = file.read()
        file_content = None
        if file_name.endswith(".pdf"):
            file_content = read_pdf(binary_content)                    
        elif file_name.endswith(".doc"):
            file_content = read_docx(binary_content)                    
        elif file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png") or file_name.endswith(".gif") or file_name.endswith(".bmp"):
            return "Unsupported file type", 400                    
        else:
            file_content = binary_content.decode('utf-8') 

        if split_method == 'text':
            if not split_value:
                return "Please provide text to split by.", 400
            sections = split_file_by_text(file_content, split_value, uploads_dir)
            split_text = f"text '{split_value}'"
        elif split_method == 'regex':
            if not split_regex:
                return "Please provide text to split by.", 400
            sections = split_file_by_regex(file_content, split_regex, uploads_dir)
            split_text = f"text '{split_value}'"
        elif split_method == 'lines':
            if not split_value.isdigit():
                return "Please provide a valid number of lines to split by.", 400
            sections = split_file_by_lines(file_content, int(split_value))
            split_text = f"{split_value} lines"
        elif split_method == 'paragraphs':
            sections = split_file_by_paragraphs(file_content)
            split_text = "paragraphs"
        else:
            return "Invalid split method", 400

        # Pass split_text to the template
        return render_template('split_results.html', sections=sections, split_text=split_text, split_method=split_method)
    
    return render_template('split_file.html')