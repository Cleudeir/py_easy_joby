import os
import fnmatch
import time
from flask import Blueprint, current_app, render_template, request, Response
from src.Modules.project_documentation.module import (get_final_summary, get_summary,
    read_and_summarize_file)
import markdown
from src.Libs.Files import read_file_content, save_content_to_file, save_image_to_file
from src.Libs.File_processor import read_docx, read_pdf

project_documentation_routes = Blueprint("project_documentation_routes", __name__, template_folder=".")


@project_documentation_routes.route(
    "/get_project_documentation", methods=["GET", "POST"]
)
def get_project_documentation():
    documentation_html = None
    
    if(request.method == "GET"):
        return render_template("project_documentation.html", documentation_html=documentation_html)

    if request.method == "POST":
        useCache = request.form.get("useCache", False)
        project_name = request.form.get("project_name", "").replace(" ", "_")        
        
        if not project_name:
            return "<p>Error: Project directory path is required.</p>"

        uploads_dir = os.path.join(current_app.root_path, "src/.outputs/" + project_name + "/")
        print(uploads_dir)
        os.makedirs(uploads_dir, exist_ok=True)
        
        files = request.files.getlist('project_path')
        for file in files:
            file_name = file.filename
            print(file_name)
            file_path = uploads_dir + file_name
            try:
                binary_content = file.read()
                content = None
                if file_name.endswith(".pdf"):
                    content = read_pdf(binary_content)                    
                elif file_name.endswith(".doc"):
                    content = read_docx(binary_content)                    
                elif file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png") or file_name.endswith(".gif") or file_name.endswith(".bmp"):
                    continue
                    save_image_to_file(file_path, binary_content)
                else:
                    content = binary_content.decode('utf-8')
                
                summary_path = file_path + ".md"
                # check if file already exists
                if os.path.exists(summary_path) and useCache:
                    content = read_file_content(summary_path)
                    continue
                               
                  
                summary = get_summary(content, file_name)
                print(summary)
                save_content_to_file(summary_path, summary)
              
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")
                
        return  '<p>Documentation generation complete.</p>'    
        try:
            def generate_documentation():
                yield "<p>Starting documentation generation...</p>\n"                
                combined_summary = ""

                for file in files:     
                    try:
                        
                        file_name = file.filename
                        print(file_name)
                        ignore_patterns = ["project_documentation.txt", "README.md"]
                        if any(fnmatch.fnmatch(file_name, pattern) for pattern in ignore_patterns):                
                            continue

                        if not file_name.startswith(".") and file_name.endswith((
                            ".py", ".txt", ".html", ".yml", ".js", ".ts", ".tsx", ".jsx", ".json", ".java"
                        )):
                            # Read file content
                            time.sleep(1)
                            content = file.read().decode('utf-8')  # Read the file content once
                            print(f"File content read: {len(content)}")
                            
                            name = file.filename
                            
                            file = {
                                "content": content,
                                "name": name
                            }                          
                            if content is not None:
                                continue
                            summary = read_and_summarize_file(file, uploads_dir, useCache)
                            combined_summary += summary
                            yield markdown.markdown(summary) + "\n"

                    except Exception as e:
                        print(f"Error reading file {file_name}: {e}")
                        continue  # Continue processing other files
                 
                # GENERATE SUMMARY
                final_summary = get_final_summary(
                    summary=combined_summary,                            
                )
                general_summary_file = f"""{final_summary}"""
                # Save the summary to a file
                save_content_to_file(
                    os.path.join(uploads_dir, "README.md"),
                    general_summary_file
                )
                # code extension code form
                general_summary_html = f"<h1>README.md</h1>\n"
                general_summary_html += markdown.markdown(final_summary)
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