import os
from src.modules.gpt import describe_image_with_ollama
import os
from flask import jsonify
from jinja2 import FileSystemLoader, Environment
from pypandoc import convert_file, convert_text

def get_images_from_path(path: str):
    """
    Reads a directory and returns a list of image file paths.
    """
    supported_formats = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
    return [
        os.path.join(path, file)
        for file in os.listdir(path)
        if os.path.isfile(os.path.join(path, file)) and os.path.splitext(file)[1].lower() in supported_formats
    ]
