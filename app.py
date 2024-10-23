from flask import Flask, render_template, request
from modules.directory_structure import get_directory_structure
from modules.ollama import get_ollama_response, get_available_models
from modules.file_processor import (
    split_file_by_text,
    split_file_by_lines,
    split_file_by_paragraphs,
    read_pdf,
    read_docx,
    read_txt,
)
import os
from flasgger import Swagger, swag_from

app = Flask(__name__)
Swagger(app)  # Initialize Swagger UI

app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    """
    Home Page
    ---
    responses:
      200:
        description: Render the home page
    """
    return render_template('index.html')

@app.route('/directory_structure', methods=['GET', 'POST'])
@swag_from({
    'methods': ['GET', 'POST'],
    'parameters': [
        {
            'name': 'directory_path',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'The path of the directory to analyze'
        }
    ],
    'responses': {
        200: {
            'description': 'Directory structure retrieved successfully',
        },
        400: {
            'description': 'Invalid directory path',
        }
    }
})
def directory_structure():
    if request.method == 'POST':
        directory_path = request.form['directory_path']
        structure = get_directory_structure(directory_path)
        return render_template('directory_structure.html', structure=structure)
    return render_template('directory_structure.html')

@app.route('/ollama', methods=['GET', 'POST'])
@swag_from({
    'methods': ['GET', 'POST'],
    'parameters': [
        {
            'name': 'model',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Model to use for Ollama response'
        },
        {
            'name': 'system_prompt',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'System prompt for the model'
        },
        {
            'name': 'user_prompt',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'User prompt for the model'
        }
    ],
    'responses': {
        200: {
            'description': 'Ollama response generated successfully',
        },
        400: {
            'description': 'Invalid input data',
        }
    }
})
def ollama():
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

@app.route('/split_file', methods=['GET', 'POST'])
@swag_from({
    'methods': ['GET', 'POST'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'File to be split'
        },
        {
            'name': 'split_method',
            'in': 'formData',
            'type': 'string',
            'enum': ['text', 'lines', 'paragraphs'],
            'required': True,
            'description': 'Method to split the file'
        },
        {
            'name': 'split_value',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Value used for splitting (e.g., number of lines or text to split by)'
        }
    ],
    'responses': {
        200: {
            'description': 'File split successfully',
        },
        400: {
            'description': 'Invalid input data',
        }
    }
})
def split_file():
    if request.method == 'POST':
        file = request.files['file']
        split_method = request.form['split_method']
        split_value = request.form.get('split_value')

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
        elif split_method == 'lines':
            if not split_value or not split_value.isdigit():
                return "Please provide a valid number of lines to split by.", 400
            sections = split_file_by_lines(file_content, int(split_value))
        elif split_method == 'paragraphs':
            sections = split_file_by_paragraphs(file_content)
        else:
            return "Invalid split method", 400

        return render_template('split_results.html', sections=sections, split_method=split_method)
    return render_template('split_file.html')

if __name__ == '__main__':
    app.run(debug=True)
