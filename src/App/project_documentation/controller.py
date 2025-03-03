from flask import Blueprint, render_template, request, Response
from src.App.project_documentation.service import (
    download_zip_files, get_directory_output, process_uploaded_files, generate_summary
)

project_documentation_routes = Blueprint("project_documentation_routes", __name__, template_folder=".")


@project_documentation_routes.route("/get_project_documentation", methods=["GET", "POST"])
def get_project_documentation():
    """Handles project documentation request"""
    if request.method == "GET":
        return render_template("view_project_documentation.html")
    if request.method == "POST":
        uploads_dir = get_directory_output(request)
        files = request.files.getlist('project_path')
        use_cache = request.form.get("useCache", False)
        read_images = request.form.get("useImage", False)
        list_content = process_uploaded_files(files, read_images)
        
        return Response(generate_summary(files, list_content, uploads_dir, use_cache,read_images), mimetype="text/html")

@project_documentation_routes.route("/project_documentation/download_all", methods=["POST"])
def download_project():
    uploads_dir = get_directory_output(request)
    return download_zip_files(uploads_dir)
