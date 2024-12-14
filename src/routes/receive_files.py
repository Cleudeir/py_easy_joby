from flask import Blueprint, current_app, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

receive_files_routes = Blueprint("receive_files_routes", __name__)


@receive_files_routes.route("/upload-folder", methods=["GET", "POST"])
def upload_folder():
    """
    Endpoint to receive and save multiple files uploaded as part of a folder.
    """
    if request.method == "GET":
        return render_template("upload_folder.html")

    files = request.files.getlist("files[]")
    # join src/.outputs/files

    if not files:
        return jsonify({"error": "No files uploaded."}), 400

    try:

        for file in files:
            filename = (
                secure_filename(file.filename).replace("_", "/").replace("//", "_")
            )
            destination_path = os.path.join(
                os.path.join(current_app.root_path, "src/.outputs/files", filename),
            )
            # create path
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            file.save(destination_path)
            # save file

        return jsonify(
            {
                "message": f"Uploaded {len(files)} files to {destination_path} successfully!"
            }
        )
    except Exception as e:
        return jsonify({"error": f"Failed to upload files: {str(e)}"}), 500
