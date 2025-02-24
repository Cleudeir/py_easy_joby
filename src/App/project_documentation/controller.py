from flask import Blueprint, render_template, request, Response
from src.App.project_documentation.service import (
    get_directory_output, process_uploaded_files, generate_summary
)

project_documentation_routes = Blueprint("project_documentation_routes", __name__, template_folder=".")


@project_documentation_routes.route("/get_project_documentation", methods=["GET", "POST"])
def get_project_documentation():
    """Handles project documentation request"""
    documentation_html = None
    
    if request.method == "GET":
        return render_template("view_project_documentation.html", documentation_html=documentation_html)

    if request.method == "POST":
        uploads_dir = get_directory_output(request)
        print('Uploads Directory:', uploads_dir)
        
        files = request.files.getlist('project_path')
        use_cache = request.form.get("useCache", False)

        list_content = process_uploaded_files(files)
        
        return Response(generate_summary(files, list_content, uploads_dir, use_cache), mimetype="text/html")
