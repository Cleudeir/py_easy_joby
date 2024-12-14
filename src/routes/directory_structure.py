from flask import Blueprint, render_template, request
from src.modules.directory_structure import get_directory_structure

directory_structure_routes = Blueprint("directory_structure_routes", __name__)


@directory_structure_routes.route("/get-directory-structure", methods=["GET", "POST"])
def get_directory_structure_route():
    if request.method == "POST":
        directory_path = request.form["directory_path"]
        structure, content = get_directory_structure(directory_path)
        html = f"{structure}</br>\n\n{content}"
        return render_template("directory_structure.html", structure=html)
    return render_template("directory_structure.html")
