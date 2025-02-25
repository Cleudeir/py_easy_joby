from flask import Blueprint,  render_template, request, Response
from src.App.reconstruction.service import (generate_documentation, get_directory_output)


reconstruction_routes = Blueprint('reconstruction_routes', __name__, template_folder='.', static_folder='static')

@reconstruction_routes.route('/reconstruction_code', methods=['GET', 'POST'])
def reconstruction_code():
    if request.method == 'GET':
         return render_template('view_reconstruction.html')

    if request.method == 'POST':
        print('reconstruction_code')
        file = request.files['file']
        filename = None
        file_content = None
        try:
            if not file:
                raise Exception('Nenhum arquivo foi selecionado')
            filename = file.filename
            file_content = file.read().decode('utf-8')
        except Exception as e:
            def error():
                yield f"<p>Error: Não foi possível ler o arquivo ({str(e)})</p>"
                return            
            return Response(error(), mimetype='text/html')
        output_path = get_directory_output(request)
        return Response(generate_documentation(filename, file_content, output_path), mimetype='text/html')


   
