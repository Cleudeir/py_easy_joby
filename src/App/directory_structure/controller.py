from flask import Blueprint, render_template, request, Response
from src.App.directory_structure.service import get_directory_structure
import time

directory_structure_routes = Blueprint("directory_structure_routes", __name__, template_folder=".")


@directory_structure_routes.route("/get-directory-structure", methods=["GET", "POST"])
def get_directory_structure_route():
    if request.method == "GET":
        return render_template("view_directory_structure.html")
    if request.method == "POST":
        files = request.files.getlist('project_path')        
        
        structure, content = get_directory_structure(files)
        
        def result():
            # check if exists files
            if not files or all(file.filename == '' for file in files):
                yield "<p>No files uploaded.</p>\n"
                return 
            sleep_time = 0.100
            yield "<p>start generation ...</p>\n"
            time.sleep(sleep_time)
            yield f"<h1>Project Structure</h1>\n<pre><code id='agent_coder'>{structure}</code></pre>"
            time.sleep(sleep_time)
            # yield f"{content}"
            time.sleep(sleep_time)
            yield "<p>Generation complete!</p>\n"            
        
        return Response(result(), mimetype="text/html")

 