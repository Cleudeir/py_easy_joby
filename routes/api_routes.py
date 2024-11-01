from flask import Blueprint, request, jsonify, current_app
from modules.directory_structure import get_directory_structure
from modules.ollama import get_ollama_response
from modules.file_processor import (
    read_pdf, read_docx, read_txt,
    split_file_by_text, split_file_by_lines, split_file_by_paragraphs
)
from flasgger import swag_from
from modules.project_documentation import generate_documentation, save_documentation
from modules.ollama import get_available_models
import os

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/get-project-documentation', methods=['POST'])
@swag_from('../swagger/get_project_documentation.yml')
def api_get_project_documentation():
    """
    API endpoint to generate project documentation.
    ---
    tags:
      - Documentation
    """
    # Fetch available models
    available_models = get_available_models()
    
    # Get project path and model from request form data
    project_path = request.form.get('project_path', '').strip()
    selected_model = request.form.get('model', '').strip()
    
    # Check if required fields are provided
    if not project_path:
        return jsonify({"error": "Project directory path is required."}), 400
    if selected_model not in available_models:
        return jsonify({"error": f"Invalid model. Available models are: {', '.join(available_models)}"}), 400

    # Define output path in uploads directory
    uploads_dir = os.path.join(current_app.root_path, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    output_path = os.path.join(uploads_dir, 'project_documentation.txt')

    try:
        # Generate documentation content
        documentation_content = generate_documentation(project_path, selected_model)
        save_documentation(output_path, documentation_content)
        return jsonify({
            "message": "Documentation generated successfully.",
            "documentation_content": documentation_content
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error generating documentation: {str(e)}"}), 500
    

@api_routes.route('/api/directory-structure', methods=['POST'])
@swag_from('../swagger/directory_structure.yml')
def api_directory_structure():
    directory_path = request.form.get('directory_path')
    if not directory_path:
        return jsonify({"error": "Directory path is required"}), 400    
    try:
        structure = get_directory_structure(directory_path)
        return jsonify(structure), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@api_routes.route('/api/ollama', methods=['POST'])
@swag_from('../swagger/ollama.yml')
def api_ollama_response():
    model = request.form.get('model')
    system_prompt = request.form.get('system_prompt')
    user_prompt = request.form.get('user_prompt')
    if not model or not system_prompt or not user_prompt:
        return jsonify({"error": "All fields are required"}), 400

    response = get_ollama_response(model, system_prompt, user_prompt)
    return jsonify(response)

@api_routes.route('/api/file-splitter', methods=['POST'])
@swag_from('../swagger/split_file.yml')
def api_file_splitter():
    file = request.files.get('file')
    split_method = request.form.get('split_method')
    split_value = request.form.get('split_value')

    # Check file type and read content
    if file.filename.endswith('.pdf'):
        file_content = read_pdf(file)
    elif file.filename.endswith('.docx'):
        file_content = read_docx(file)
    elif file.filename.endswith('.txt'):
        file_content = read_txt(file)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    # Initialize sections and split_text for response
    sections = []
    split_text = ""

    # Perform splitting based on method
    if split_method == 'text':
        if not split_value:
            return jsonify({"error": "Please provide text to split by."}), 400
        sections = split_file_by_text(file_content, split_value)
        split_text = f"text '{split_value}'"
    elif split_method == 'lines':
        if not split_value or not split_value.isdigit():
            return jsonify({"error": "Please provide a valid number of lines to split by."}), 400
        sections = split_file_by_lines(file_content, int(split_value))
        split_text = f"{split_value} lines"
    elif split_method == 'paragraphs':
        sections = split_file_by_paragraphs(file_content)
        split_text = "paragraphs"
    else:
        return jsonify({"error": "Invalid split method"}), 400

    # Return response with sections and split_text
    return jsonify({
        "sections": sections,
        "split_text": split_text
    })
