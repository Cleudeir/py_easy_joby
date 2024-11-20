from flask import Blueprint, render_template, request, Response
from src.modules.agent_summary_reconstruction_code import (
    get_agent_coder,
    get_agent_fix_summary,
    get_agent_similarity,
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
