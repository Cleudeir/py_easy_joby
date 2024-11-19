import fnmatch
import shutil
import time
from flask import Blueprint, render_template, request, current_app, Response, jsonify, stream_with_context
from src.modules.image_description import  get_images_from_path, describe_image_with_gemini
from src.modules.refactor import get_agent_separate
from src.modules.agent_summary_reconstruction_code import get_agent_coder, get_agent_fix_summary, get_agent_similarity, get_agent_summary, get_agent_improvement
from src.modules.directory_structure import get_directory_structure
from src.modules.gpt import get_ollama_models, get_ollama_response
from src.modules.file_processor import (
    read_pdf, read_docx, read_txt,
    split_file_by_text, split_file_by_lines, split_file_by_paragraphs
)
from src.modules.project_documentation import  get_project_files, read_and_summarize_file, summarize_with_ollama_final
import os
import markdown

html_routes = Blueprint('html_routes', __name__)

@html_routes.route('/')
def home():
    """Home Page"""
    return render_template('index.html')

@html_routes.route("/process-images", methods=["POST", "GET"])
def image_description():
    if request.method == "GET":
        return render_template("image_description.html")

    elif request.method == "POST":
        data = request.json
        input_path = data.get("path")
        output_path = os.path.join(current_app.root_path, 'src/.outputs' + input_path)
        static_image_path = os.path.join(current_app.root_path, 'src/static/images')
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(static_image_path, exist_ok=True)
    
    try:
        # Get all images in the directory
        images = get_images_from_path(input_path)

        def render():
            
            yield "<p>Starting documentation generation...</p>\n"
            docx_html = ''
            
            for img in images:
      

                # Copy image to the static folder 
                path_to_copy = os.path.join(static_image_path, os.path.basename(img))
                shutil.copyfile(img, path_to_copy)
                
                url_image = os.path.join('static/images', os.path.basename(img))
                print(f"Image saved: {url_image}")
                html_image = f"<img src='{url_image}' alt='{os.path.basename(url_image)}' style='max-width: 100%; height: auto;' />"
                # width 50% higth proporcional
                docx_html += f"<img src='{img}' alt='{os.path.basename(img)}'width='50%' height='50%' object-fit='contain'/>"
                yield html_image
                # check if exists html file
                if os.path.exists(os.path.join(output_path, os.path.basename(img).split('.')[0] + '.html')):
                    #read file
                    with open(os.path.join(output_path, os.path.basename(img).split('.')[0] + '.html'), 'r') as f:
                        content = f.read()
                        docx_html += content
                        yield content
                    continue
                    
                # Generate the description using your Ollama integration
                markdown_text = describe_image_with_gemini(img)
                html_text = markdown.markdown(markdown_text, extensions=['extra', 'tables'])
          
                
                docx_html += html_text
                file_html = os.path.join(output_path, os.path.basename(img).split('.')[0] + '.html')
                with open(file_html, 'w') as f:
                    f.write(html_text)
                yield html_text
            docx_file = os.path.join(output_path, 'project_documentation.docx')
            with open(docx_file, 'wb') as f:
                f.write(docx_html.encode('utf-8'))
            time.sleep(0.100)            
            yield "<p>Documentation generation complete.</p>\n"
            
        return Response(stream_with_context(render()), mimetype='text/html')

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@html_routes.route('/refactor', methods=['GET', 'POST'])
def refactor():
    available_models = get_ollama_models()
    documentation_html = None

    if request.method == 'POST':
        selected_model = request.form.get('model', '').strip()
        gpt_provider = request.form.get('gpt_provider', '').strip()
        file = request.files['file']
        file_content = None
        
        try:
            file_content = file.read().decode('utf-8')         
        except Exception as e:
            documentation_html = f"<p>Error: Não foi possível ler o arquivo ({str(e)})</p>"            
            return Response(documentation_html, mimetype='text/html')
        
        try:
            # Generate documentation in chunks
            def generate_documentation():
                yield "<p>Starting documentation generation...</p>\n"
                time.sleep(0.100)
                yield markdown.markdown(f"<pre><code id='agent_coder'>{file_content.replace('<', '&lt;')}</code></pre>")
                time.sleep(0.100)
                
                coder = get_agent_separate(gpt_provider, selected_model, file_content)
                yield markdown.markdown(f"<pre><code id='agent_coder'>{coder.replace('<', '&lt;')}</code></pre>")
                
                agent_evaluation = get_agent_similarity(file_content, coder)
                yield markdown.markdown(f'Agent evaluation: {agent_evaluation}')
                
                time.sleep(0.100)
                yield "<p>Summary generation complete</p>\n" 
                print("Documentation generation complete.")
            
            return Response(generate_documentation(), mimetype='text/html')

        except Exception as e:
            error_message = f"Error generating documentation: {str(e)}"
            documentation_html = f"<p>{error_message}</p>"
            return render_template('agent_summary_reconstruction_code.html', documentation_html=documentation_html, models=available_models)
    
    return render_template('agent_summary_reconstruction_code.html', documentation_html=documentation_html, models=available_models)

@html_routes.route('/agent_summary_reconstruction_code', methods=['GET', 'POST'])
def agent_summary_reconstruction_code():
    available_models = get_ollama_models()
    documentation_html = None

    if request.method == 'POST':
        selected_model = request.form.get('model', '').strip()
        gpt_provider = request.form.get('gpt_provider', '').strip()
        file = request.files['file']
        file_content = None
        
        try:
            file_content = file.read().decode('utf-8')         
        except Exception as e:
            documentation_html = f"<p>Error: Não foi possível ler o arquivo ({str(e)})</p>"            
            return Response(documentation_html, mimetype='text/html')
        
        try:
            # Generate documentation in chunks
            def generate_documentation():
                yield "<p>Starting documentation generation...</p>\n"
                time.sleep(0.100)
                yield markdown.markdown(f"<pre><code id='agent_coder'>{file_content.replace('<', '&lt;')}</code></pre>")
                time.sleep(0.100)
                
                current_summary = get_agent_summary(gpt_provider, selected_model, file_content)
                yield markdown.markdown(current_summary)
                
                agent_evaluation = 0
                evaluation_min = 0.65
                while agent_evaluation < evaluation_min:              
                    agent_coder = get_agent_coder(gpt_provider, selected_model, current_summary)
                    yield f"<pre><code id='agent_coder'>{agent_coder.replace('<', '&lt;')}</code></pre>"
                    
                    agent_evaluation = get_agent_similarity(file_content, agent_coder)
                    yield markdown.markdown(f'Agent evaluation: {agent_evaluation}')
                    
                    if(agent_evaluation < evaluation_min):
                        agent_improvement = get_agent_improvement(gpt_provider, selected_model, file_content, current_summary)
                        yield markdown.markdown(agent_improvement)  
                        
                        current_summary = get_agent_fix_summary(gpt_provider, selected_model, file_content, current_summary, agent_improvement)
                        yield markdown.markdown(current_summary)                  

                time.sleep(0.100)
                yield "<p>Summary generation complete</p>\n" 
                print("Documentation generation complete.")
            
            return Response(generate_documentation(), mimetype='text/html')

        except Exception as e:
            error_message = f"Error generating documentation: {str(e)}"
            documentation_html = f"<p>{error_message}</p>"
            return render_template('agent_summary_reconstruction_code.html', documentation_html=documentation_html, models=available_models)
    
    return render_template('agent_summary_reconstruction_code.html', documentation_html=documentation_html, models=available_models)

@html_routes.route('/get_project_documentation', methods=['GET', 'POST'])
def get_project_documentation_route():
    available_models = get_ollama_models()
    documentation_html = None

    if request.method == 'POST':
        project_path = request.form.get('project_path', '').strip()
        selected_model = request.form.get('model', '').strip()
        gpt_provider = request.form.get('gpt_provider', '').strip()
        uploads_dir = os.path.join(current_app.root_path, 'src/.outputs' + project_path)

        if not project_path:
            documentation_html = "<p>Error: Project directory path is required.</p>"
            return render_template('project_documentation.html', documentation_html=documentation_html, models=available_models)

        os.makedirs(uploads_dir, exist_ok=True)

        try:
            def generate_documentation():
                yield "<p>Starting documentation generation...</p>\n"
                ignore_patterns = ["project_documentation.txt"]
                combined_content = ""

                for file_path in get_project_files(project_path):
                    file_name = os.path.basename(file_path)
                    if any(fnmatch.fnmatch(file_name, pattern) for pattern in ignore_patterns):
                        continue

                    summary = read_and_summarize_file(file_path, gpt_provider, selected_model, uploads_dir)
                    combined_content += summary
                    yield markdown.markdown(summary) + "\n"

                # Generate README and LinkedIn post
                structure = get_directory_structure(project_path)
                combined_content = f"{combined_content}\n\n## Project structure:\n{structure}"
                general_summary = summarize_with_ollama_final(content=combined_content, filename='README.md', gpt_provider=gpt_provider, model=selected_model)
                #save Readme
                with open(os.path.join(uploads_dir, 'README.md'), 'w') as f:
                    f.write(general_summary)
                yield markdown.markdown(general_summary)
                time.sleep(0.100)
                yield "<p>Documentation generation complete.</p>\n"
                print("Documentation generation complete.")

            return Response(generate_documentation(), mimetype='text/html')

        except Exception as e:
            error_message = f"Error generating documentation: {str(e)}"
            documentation_html = f"<p>{error_message}</p>"
            return render_template('project_documentation.html', documentation_html=documentation_html, models=available_models)
    
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

