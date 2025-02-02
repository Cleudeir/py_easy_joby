import os
import fnmatch
import time
from flask import Blueprint, current_app, render_template, request, Response
from src.Modules.project_documentation.module import (get_final_summary, get_summary,
    get_summary_fix_follow)
import markdown
from src.Libs.Files import read_file_content, save_content_to_file, save_image_to_file
from src.Libs.File_processor import read_docx, read_pdf
from src.Libs.Time import time_format_string

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
       
        list_content = []
         
        files = request.files.getlist('project_path')
        for file in files:
            file_name = file.filename
            try:                
                binary_content = file.read()
                content = None
                if file_name.endswith(".pdf"):
                    content = read_pdf(binary_content)                    
                elif file_name.endswith(".doc"):
                    content = read_docx(binary_content)                    
                elif file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png") or file_name.endswith(".gif") or file_name.endswith(".bmp"):
                    continue                    
                else:
                    content = binary_content.decode('utf-8')      
                list_content.append({
                    "file_name": file_name,
                    "content": content
                })           
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")
        
     
       
        def generate_summary():
            combined_summary = ""
            yield "<p>Starting documentation generation...</p>\n"
            delay = 0.100
            for content in list_content:
                start_time = time.time()
                file_name = content["file_name"]
                file_path = uploads_dir + file_name
                summary_path = file_path + ".md"          
                summary = None
                
                if os.path.exists(summary_path) and useCache:
                    summary = read_file_content(summary_path)
                else:                     
                    summary = get_summary(content)
                    save_content_to_file(summary_path, summary)
                    
                combined_summary += f"## {file_name}\n\n{summary}\n\n"
                yield markdown.markdown(f"<p>Creating summary for : <strong>{file_name}</strong></p> ")
                
                elapsed_time = time_format_string(start_time)
                yield markdown.markdown(f"{summary}\n<p>Time render: <strong>{elapsed_time}</strong></p>\n")
                
            final_summary = get_final_summary(
                summary=combined_summary,                            
            )   
            time.sleep(delay)
            start_time = time.time()
            elapsed_time = time_format_string(start_time)
            yield markdown.markdown(f"<p>Creating summary for : <strong>Readme.md</strong></p> ") 
            yield markdown.markdown(f"{final_summary}\n<p>Time render: <strong>{elapsed_time}</strong></p>\n")
                      
            save_content_to_file(
                uploads_dir + "README.md",
                final_summary
            )
            
            yield "<p>Summary generation complete</p>\n"
        
        return Response(generate_summary(), mimetype="text/html")
     