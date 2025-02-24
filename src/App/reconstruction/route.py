import os
from flask import Blueprint,  render_template, request, Response
from src.App.reconstruction.module import (get_agent_coder, get_agent_fix_code,
    get_agent_fix_summary, get_agent_improvement, get_agent_summary)
import markdown
import time
from src.Libs.Files import save_content_to_file

reconstruction_routes = Blueprint('reconstruction_routes', __name__, template_folder='.', static_folder='static')

@reconstruction_routes.route('/reconstruction_code', methods=['GET', 'POST'])
def reconstruction_code():
    documentation_html = None
    
    if request.method == 'GET':
         return render_template('reconstruction.html', documentation_html=documentation_html)

    if request.method == 'POST':
        file = None
        file_content = None     
        try:   
            file   = request.files['file']     
            file_content = file.read().decode('utf-8')
        except Exception as e:
            documentation_html = f"<p>Error: Não foi possível ler o arquivo ({str(e)})</p>"
            return Response(documentation_html, mimetype='text/html')

        try:
            def generate_documentation():
                if file.filename == '':
                    yield "<p>No file uploaded</p>\n"
                    return  
                yield "<p>Starting documentation generation...</p>\n"
                time.sleep(0.100)
                yield markdown.markdown(f"<pre><code id='agent_coder'>{file_content.replace('<', '&lt;')}</code></pre>")
                time.sleep(0.100)            
                
                summary = get_agent_summary(file_content)
                yield markdown.markdown(summary)

                code = get_agent_coder(summary)
                yield f"<pre><code id='agent_coder'>{code.replace('<', '&lt;')}</code></pre>"

                agent_improvement = get_agent_improvement(file_content, code)
                yield markdown.markdown(agent_improvement)
                
                summary = get_agent_fix_summary(summary, agent_improvement)
                yield markdown.markdown(summary)

                code = get_agent_fix_code(code, agent_improvement)
                yield f"<pre><code id='agent_coder'>{code.replace('<', '&lt;')}</code></pre>"

                time.sleep(0.100)
                yield "<p>Summary generation complete</p>\n"
                
                file_name, file_extension = f"{file.filename}".split('.')
                root_path = os.path.dirname(os.path.abspath(__file__)).split('src')[0]
            
                save_path = os.path.join(root_path, 'src/.outputs/reconstruction_code/')          
               
                file_resume = os.path.join(save_path, file_name + '.md')

                
                save_content_to_file(file_resume, summary)

                file_code_reconstruction = os.path.join(save_path, file_name + file_extension)
                save_content_to_file(file_code_reconstruction, code)

            return Response(generate_documentation(), mimetype='text/html')

        except Exception as e:
            error_message = f"Error generating documentation: {str(e)}"
            documentation_html = f"<p>{error_message}</p>"
            return render_template('reconstruction.html', documentation_html=documentation_html)

   
