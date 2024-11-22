import os
from flask import Blueprint, current_app, render_template, request, Response
from src.modules.agent_summary_reconstruction_code import (
    get_agent_coder,
    get_agent_fix_summary,
    get_agent_summary,
    get_agent_improvement,
)
from src.modules.gpt import get_ollama_models
import markdown
import time

agent_summary_reconstruction_routes = Blueprint('agent_summary_reconstruction_routes', __name__)

@agent_summary_reconstruction_routes.route('/agent_summary_reconstruction_code', methods=['GET', 'POST'])
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
            def generate_documentation():
                yield "<p>Starting documentation generation...</p>\n"
                time.sleep(0.100)
                yield markdown.markdown(f"<pre><code id='agent_coder'>{file_content.replace('<', '&lt;')}</code></pre>")
                time.sleep(0.100)
                
                summary = 'testes'
                code = 'testes'
                
                summary = get_agent_summary(gpt_provider, selected_model, file_content)
                yield markdown.markdown(summary)

                code = get_agent_coder(gpt_provider, selected_model, summary)
                yield f"<pre><code id='agent_coder'>{code.replace('<', '&lt;')}</code></pre>"

                agent_improvement = get_agent_improvement(gpt_provider, selected_model, file_content, summary)
                yield markdown.markdown(agent_improvement)

                summary = get_agent_fix_summary(gpt_provider, selected_model, file_content, summary, agent_improvement)
                yield markdown.markdown(summary)

                code = get_agent_coder(gpt_provider, selected_model, summary)
                yield f"<pre><code id='agent_coder'>{code.replace('<', '&lt;')}</code></pre>"

                time.sleep(0.100)
                yield "<p>Summary generation complete</p>\n"
                
                file_name, file_extension = f"{file.filename}".split('.')
                root_path = os.path.dirname(os.path.abspath(__file__)).split('src')[0]
                print(root_path)
                save_path = os.path.join(root_path, 'src/.outputs/reconstruction_code/')          
                os.makedirs(save_path, exist_ok=True)

                file_resume = os.path.join(save_path, file_name + '.md')
              
                with open(file_resume, 'w') as f:
                    f.write(summary)


                file_code_reconstruction = os.path.join(save_path, file_name + file_extension)
              
                with open(file_code_reconstruction, 'w') as f:
                    f.write(code)
    

                 

            return Response(generate_documentation(), mimetype='text/html')

        except Exception as e:
            error_message = f"Error generating documentation: {str(e)}"
            documentation_html = f"<p>{error_message}</p>"
            return render_template('agent_summary_reconstruction_code.html', documentation_html=documentation_html, models=available_models)

    return render_template('agent_summary_reconstruction_code.html', documentation_html=documentation_html, models=available_models)
