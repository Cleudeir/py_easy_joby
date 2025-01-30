from flask import Blueprint, render_template, request, Response
from src.modules.refactor import get_agent_separate, get_agent_similarity
import markdown
import time

refactor_routes = Blueprint('refactor_routes', __name__)

@refactor_routes.route('/refactor', methods=['GET', 'POST'])
def refactor():
    
    documentation_html = None

    if request.method == 'POST':
        gpt_provider = request.form.get('gpt_provider', '').strip()
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
                
                coder = get_agent_separate(gpt_provider, file_content)
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
            return render_template('agent_summary_reconstruction_code.html', documentation_html=documentation_html)
    
    return render_template('agent_summary_reconstruction_code.html', documentation_html=documentation_html)

