import re
import os
import pdfplumber
import docx
import io

def split_file_by_text(file_content, split_text, uploads_dir):
    sections = file_content.split(split_text)
    insertSplit_text = []
    for index in range(len(sections)):
        section = sections[index]
        content = f"{split_text} {section}"
        save_content_to_file(f"{uploads_dir}/{index+1}.txt", content)
        insertSplit_text.append(content)        
    return insertSplit_text

def split_file_by_regex(file_content, regex, uploads_dir):   
    sections = re.findall(regex, file_content, re.DOTALL)  
    print("sections", sections)
    insertSplit_text = []
    for index in range(len(sections)):
        section = sections[index]
        content = f"{section}"
        save_content_to_file(f"{uploads_dir}/{index+1}.txt", content)
        insertSplit_text.append(content)        
    return insertSplit_text

def split_file_by_lines(file_content, lines_per_section):
    lines = file_content.splitlines()
    sections = [lines[i:i+lines_per_section] for i in range(0, len(lines), lines_per_section)]
    return ['\n'.join(section) for section in sections]

def split_file_by_paragraphs(file_content):
    paragraphs = file_content.split('\n')
    return paragraphs

def read_pdf(file):
    text = ""
    with pdfplumber.open(io.BytesIO(file)) as pdf:  # Wrap bytes in BytesIO
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def read_docx(file):
    doc = docx.Document(io.BytesIO(file))  # Wrap bytes in BytesIO
    return '\n'.join([para.text for para in doc.paragraphs])

def read_txt(file):
    return file.read().decode('utf-8')

def create_folder_by_file_path(file_path: str) -> None:
    try:
        folder_path = os.path.dirname(file_path)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created at {folder_path}")
    except Exception as e:
        print(f"Error creating folder: {e}")
    
def save_content_to_file(file_path: str, content: str) -> None:
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)
        # print(f"Content saved to {file_path}")
    except Exception as e:
        print(f"Error saving content to file: {e}")

def save_image_to_file(file_path: str, image_binary: bytes) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as img_file:
            img_file.write(image_binary)
        print(f"Image saved to {file_path}")
    except Exception as e:
        print(f"Error saving image to file: {e}")

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""
def read_file_binary_content(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def list_files_in_folder(folder_path: str, include_subfolders: bool = False) -> list:
    file_list = []
    try:
        for root, _, files in os.walk(folder_path) if include_subfolders else [(folder_path, [], os.listdir(folder_path))]:
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    file_list.append(file_path)
        return file_list
    except Exception as e:
        print(f"Error listing files in folder: {e}")
        return []

def read_files_by_extension(folder_path: str, extension: str, include_subfolders: bool = False) -> dict:
    files_content = {}
    try:
        for root, _, files in os.walk(folder_path) if include_subfolders else [(folder_path, [], os.listdir(folder_path))]:
            for file in files:
                if file.endswith(extension):
                    file_path = os.path.join(root, file)
                    files_content[file_path] = read_file_content(file_path)
        return files_content
    except Exception as e:
        print(f"Error reading files by extension: {e}")
        return {}

def read_all_files_in_folder(folder_path: str, include_subfolders: bool = False) -> dict:
    files_content = {}
    try:
        for root, _, files in os.walk(folder_path) if include_subfolders else [(folder_path, [], os.listdir(folder_path))]:
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    files_content[file_path] = read_file_content(file_path)
        return files_content
    except Exception as e:
        print(f"Error reading all files in folder: {e}")
        return {}
