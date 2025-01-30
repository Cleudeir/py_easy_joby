import io
import os
import shutil
import time
from PIL import Image
from flask import Blueprint, render_template, request, current_app, Response, jsonify, stream_with_context
from src.modules.image_description import describe_image_with_ollama, get_images_from_path, describe_image_with_gemini
import markdown

image_description_routes = Blueprint('image_description_routes', __name__)

@image_description_routes.route("/process-images", methods=["POST", "GET"])
def image_description():
    if request.method == "GET":
        return render_template("image_description.html")

    elif request.method == "POST":
        data = request.json
        input_path = data.get("path")
        gpt_provider = data.get('provider', '').strip()
        useCache = data.get("useCache", False)        
        output_path = os.path.join(current_app.root_path, 'src/.outputs' + input_path)
        static_image_path = os.path.join(current_app.root_path, 'src/static/images')
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(static_image_path, exist_ok=True)
    try:
        # Get all images in the directory
        images = get_images_from_path(input_path)
       
        def render():
            if(len(images) == 0):
                yield "<p>No images found in the directory.</p>\n"
                return
            yield "<p>Starting documentation generation...</p>\n"
            docx_html = ''
          
            for img in images:
                path_to_copy = os.path.join(static_image_path, os.path.basename(img))
                shutil.copyfile(img, path_to_copy)
                
                url_image = os.path.join('static/images', os.path.basename(img))
                print(f"Image saved: {url_image}")
                # get dimensions of the image
                with open(img, 'rb') as f:
                    image_data = f.read()
                    image = Image.open(io.BytesIO(image_data))
                    width, height = image.size
                    proportions = width/height
                    print(f"Image proportions: {proportions}")
                    if(proportions > 1):
                        docx_html += f"<img src='{img}' alt='{os.path.basename(img)}'width='{650}px' height='{650 / proportions }px'/>"
                    else:
                        docx_html += f"<img src='{img}' alt='{os.path.basename(img)}'width='{800 * proportions}px' height='{800}px'/>"
                    
                html_image = f"<img src='{url_image}' alt='{os.path.basename(url_image)}' style='max-width: 100%; height: auto;' />"
          
                
                yield html_image
                
                document_html = os.path.join(output_path, os.path.basename(img).split('.')[0] + '.html')
                if os.path.exists(document_html) and useCache:                    
                    with open(document_html, 'r') as f:
                        content = f.read()
                        docx_html += content
                        yield content
                    continue
                markdown_text = ''
                if(gpt_provider == 'gemini'):
                    markdown_text = describe_image_with_gemini([img])
                elif(gpt_provider == 'ollama'):
                    markdown_text = describe_image_with_ollama([img])
                html_text = markdown.markdown(markdown_text, extensions=['extra', 'tables'])
                docx_html += html_text
                file_html = document_html
                with open(file_html, 'w') as f:
                    f.write(html_text)
                yield html_text
                time.sleep(0.100)  
            docx_file = os.path.join(output_path, 'project_documentation.docx')
            with open(docx_file, 'wb') as f:
                f.write(docx_html.encode('utf-8'))
            # command Linux open docx
            try:
                os.system(f"LibreOffice {docx_file}")
            except:
                print("LibreOffice not found")
            
            time.sleep(0.100)            
            yield "<p>Documentation generation complete.</p>\n"
            
        return Response(stream_with_context(render()), mimetype='text/html')

    except Exception as e:
        return jsonify({"error": str(e)}), 500
