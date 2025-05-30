from flask import Blueprint, render_template, request, Response
from src.Libs.LLM.Provider import get_text
from src.App.directory_structure.service import get_directory_structure
import time

directory_structure_routes = Blueprint("directory_structure_routes", __name__, template_folder=".")


@directory_structure_routes.route("/get-directory-structure", methods=["GET", "POST"])
def get_directory_structure_route():
    print("get_directory_structure_route")
    if request.method == "GET":
        return render_template("view_directory_structure.html")
    if request.method == "POST":
        files = request.form.getlist('project_path')

        structure = get_directory_structure(files)
        
        def result():
            # check if exists files
            if not files or all(file == '' for file in files):
                yield "<p>No files uploaded.</p>\n"
                return 
            sleep_time = 1
            yield "<p>start generation ...</p>\n"
            time.sleep(sleep_time)
            yield f"""<h1>Project Structure</h1>
            <pre>
            <code id='agent_coder'>
            {structure}
            </code>
            </pre>"""
            time.sleep(sleep_time)
            explains_structure = get_text("Explain the system design or architecture apply in this code , response in once paragraph, in layman's terms, not use code or comments", structure) 
            yield f"<h1>Explains Structure</h1>\n{explains_structure}"
            time.sleep(sleep_time)
            yield "<p>Generation complete!</p>\n"            
        
        return Response(result(), mimetype="text/html")

 