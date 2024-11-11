import fnmatch
from flask import Blueprint, Response, json, request, jsonify, current_app
from src.modules.project_documentation import get_project_files, read_and_summarize_file, summarize_with_ollama_final
from src.modules.directory_structure import get_directory_structure
from src.modules.gpt import get_ollama_response
from src.modules.file_processor import (
    read_pdf, read_docx, read_txt,
    split_file_by_text, split_file_by_lines, split_file_by_paragraphs
)
from flasgger import swag_from
import os

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/get-project-documentation', methods=['POST'])
@swag_from('../swagger/get_project_documentation.yml')
def get_project_documentation_api():    
    # Get request data
    data = request.json
    project_path = data.get('project_path', '').strip()
    selected_model = data.get('model', '').strip()
    gpt_provider = data.get('gpt_provider', '').strip()
    uploads_dir = os.path.join(current_app.root_path, 'src/uploads', project_path)

    # Validate request
    if not project_path:
        return jsonify({"error": "Project directory path is required."}), 400
    
    # Create uploads directory if it doesn't exist
    os.makedirs(uploads_dir, exist_ok=True)

    try:
        # Stream the response as each summary is generated
        def generate_documentation():
            ignore_patterns = ["project_documentation.txt"]
            documentation_content = []

            yield json.dumps({"status": "Starting documentation generation..."}) + "\n"

            for file_path in get_project_files(project_path):
                file_name = os.path.basename(file_path)
                if any(fnmatch.fnmatch(file_name, pattern) for pattern in ignore_patterns):
                    continue

                # Read and summarize file
                summary = read_and_summarize_file(file_path, gpt_provider, selected_model, uploads_dir)
                documentation_content.append(summary)
                yield json.dumps({"file": file_name, "summary": summary}) + "\n"

            # Generate README and LinkedIn post
            structure = get_directory_structure(project_path)
            combined_content = f"{''.join(documentation_content)}\n\n## Project structure:\n{structure}"
            general_summary = summarize_with_ollama_final(content=combined_content, filename='README.md', gpt_provider=gpt_provider, model=selected_model)

            yield json.dumps({"general_summary": general_summary}) + "\n"
            yield json.dumps({"status": "Documentation generation complete."}) + "\n"

        return Response(generate_documentation(), mimetype='application/json')

    except Exception as e:
        error_message = f"Error generating documentation: {str(e)}"
        return jsonify({"error": error_message}), 500

    

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
