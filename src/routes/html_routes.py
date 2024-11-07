from flask import Blueprint, render_template, request, current_app
from src.modules.directory_structure import get_directory_structure
from src.modules.gpt import get_ollama_models, get_ollama_response
from src.modules.file_processor import (
    read_pdf, read_docx, read_txt,
    split_file_by_text, split_file_by_lines, split_file_by_paragraphs
)
from src.modules.project_documentation import generate_documentation, summarize_with_ollama_final
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
    available_models = get_ollama_models()

    if request.method == 'POST':
        project_path = request.form.get('project_path', '').strip()
        selected_model = request.form.get('model', '').strip()
        gpt_provider = request.form.get('gpt_provider', '').strip()

        uploads_dir = os.path.join(current_app.root_path, 'uploads')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)   

        if not project_path:
            documentation_html = "<p>Erro: O caminho do diretório do projeto é obrigatório.</p>"
            return render_template('project_documentation.html', documentation_html=documentation_html, models=available_models)

        try:
            # Gera o conteúdo da documentação com o modelo selecionado
            documentation_content = generate_documentation(project_path, gpt_provider, selected_model)          
            documentation_html = markdown.markdown(documentation_content)

            # Utiliza read_and_summarize_file para gerar o resumo geral
            general_summary = summarize_with_ollama_final(content=documentation_content, filename='README.md', gpt_provider=gpt_provider, model=selected_model )
            documentation_html += markdown.markdown(general_summary)
        except Exception as e:
            error_message = f"Erro ao gerar a documentação: {str(e)}"
            documentation_html = f"<p>{error_message}</p>"
    else:
        documentation_html = None

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
    models = get_ollama_models()
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

