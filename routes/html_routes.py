from flask import Blueprint, render_template, request, current_app
from modules.directory_structure import get_directory_structure
from modules.ollama import get_available_models, get_ollama_response
from modules.file_processor import (
    read_pdf, read_docx, read_txt,
    split_file_by_text, split_file_by_lines, split_file_by_paragraphs
)
from modules.project_documentation import generate_documentation, save_documentation
import os
import markdown
html_routes = Blueprint('html_routes', __name__)

@html_routes.route('/')
def home():
    """Home Page"""
    return render_template('index.html')

@html_routes.route('/get-project-documentation', methods=['GET', 'POST'])
def get_project_documentation_route():
    documentation_html = None
    available_models = get_available_models()  # Fetch available models

    if request.method == 'POST':
        project_path = request.form.get('project_path', '').strip()
        selected_model = request.form.get('model', '').strip()
        uploads_dir = os.path.join(current_app.root_path, 'uploads')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        output_path = os.path.join(uploads_dir, 'project_documentation.txt')

        if not project_path:
            documentation_html = "<p>Error: Project directory path is required.</p>"
            return render_template('project_documentation.html', documentation_html=documentation_html, models=available_models)

        try:
            # Generate concatenated documentation content with selected model
            documentation_content = generate_documentation(project_path, selected_model)
            save_documentation(output_path, documentation_content)
            # Parse the markdown content into HTML
            documentation_html = markdown.markdown(documentation_content)
        except Exception as e:
            error_message = f"Error generating documentation: {str(e)}"
            documentation_html = f"<p>{error_message}</p>"
    else:
        documentation_html = None  # Ensure it's None if not a POST request

    return render_template('project_documentation.html', documentation_html=documentation_html, models=available_models)

@html_routes.route('/get-directory-structure', methods=['GET', 'POST'])
def get_directory_structure_route():
    if request.method == 'POST':
        directory_path = request.form['directory_path']
        structure = get_directory_structure(directory_path)
        return render_template('directory_structure.html', structure=structure)
    return render_template('directory_structure.html')

@html_routes.route('/ollama-response', methods=['GET', 'POST'])
def ollama_response():
    models = get_available_models()
    if request.method == 'POST':
        model = request.form['model']
        system_prompt = request.form['system_prompt']
        user_prompt = request.form['user_prompt']

        response = get_ollama_response(model, system_prompt, user_prompt)
        return render_template(
            'ollama.html',
            response=response,
            model=model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            models=models
        )
    return render_template('ollama.html', models=models)

@html_routes.route('/file-splitter', methods=['GET', 'POST'])
def file_splitter():
    if request.method == 'POST':
        file = request.files['file']
        split_method = request.form['split_method']
        split_value = request.form.get('split_value', '')

        if file.filename.endswith('.pdf'):
            file_content = read_pdf(file)
        elif file.filename.endswith('.docx'):
            file_content = read_docx(file)
        elif file.filename.endswith('.txt'):
            file_content = read_txt(file)
        else:
            return "Unsupported file type", 400

        if split_method == 'text':
            if not split_value:
                return "Please provide text to split by.", 400
            sections = split_file_by_text(file_content, split_value)
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

