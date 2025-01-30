import os
import fnmatch
import time
from flask import Blueprint, current_app, render_template, request, Response
from src.modules.project_documentation import (
    get_project_files,
    read_and_summarize_file,
    get_generic_summary,
)
from src.modules.directory_structure import get_directory_structure
from Libs.LLM.Provider import get_ollama_models
import markdown

project_documentation_routes = Blueprint("project_documentation_routes", __name__)


@project_documentation_routes.route(
    "/get_project_documentation", methods=["GET", "POST"]
)
def get_project_documentation():
    documentation_html = None

    if request.method == "POST":
        print(request.form)
        project_path = request.form.get("project_path", "").strip()
        gpt_provider = request.form.get("gpt_provider", "").strip()
        uploads_dir = os.path.join(current_app.root_path, "src/.outputs" + project_path)
        useCache = request.form.get("useCache", False)

        if not project_path:
            documentation_html = "<p>Error: Project directory path is required.</p>"
            return render_template(
                "project_documentation.html",
                documentation_html=documentation_html,                
            )

        os.makedirs(uploads_dir, exist_ok=True)

        try:

            def generate_documentation():
                yield "<p>Starting documentation generation...</p>\n"
                ignore_patterns = ["project_documentation.txt"]
                combined_summary = ""

                for file_path in get_project_files(project_path):
                    file_name = os.path.basename(file_path)

                    if any(
                        fnmatch.fnmatch(file_name, pattern)
                        for pattern in ignore_patterns
                    ):
                        continue

                    summary = read_and_summarize_file(
                        file_path, gpt_provider, uploads_dir, useCache
                    )
                    combined_summary += summary
                    yield markdown.markdown(summary) + "\n"

                # GENERATE SUMMARY
                general_summary = get_generic_summary(
                    summary=combined_summary,
                    gpt_provider=gpt_provider,              
                )
                general_summary_file = f"""{general_summary}"""
                # Save the summary to a file
                with open(os.path.join(uploads_dir, "README.md"), "w") as f:
                    f.write(general_summary_file)
                # code extension code form
                general_summary_html = f"<h1>README.md</h1>\n"
                general_summary_html += markdown.markdown(general_summary)
                yield general_summary_html
                time.sleep(0.100)

                yield "<p>Documentation generation complete.</p>\n"
                print("Documentation generation complete.")

            return Response(generate_documentation(), mimetype="text/html")

        except Exception as e:
            error_message = f"Error generating documentation: {str(e)}"
            documentation_html = f"<p>{error_message}</p>"
            return render_template(
                "project_documentation.html",
                documentation_html=documentation_html,
              
            )

    return render_template(
        "project_documentation.html",
        documentation_html=documentation_html,     
    )
