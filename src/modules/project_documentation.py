import os
from src.modules.file_processor import read_pdf, read_docx
from src.modules.ollama import get_ollama_response
import fnmatch

def summarize_with_ollama(content, filename, model):
    """
    Summarizes the content of a file using an Ollama model and returns it in Markdown format,.
    """
    system_prompt = """
    Você é um assistente útil que resume arquivos. Seja direto em suas respostas, não crie comentários. Responda em formatado em Markdown, mas não use ```Markdown``` e Responda em Português (Br). Use a estrutura:

    - **Objetivo do Código**: Descrição breve da finalidade do código.

    - **Lógica Central**:
    - Resumo dos principais lógica implementada.

    - **Bibliotecas**:
    - Liste todas as bibliotecas usadas no código.

    - **Métodos**:
    - Liste todos os métodos/funções usados no código, com nome, argumentos de entrada, retorno .

    Se o arquivo não se tratar de código, faça apenas o resumo.
    """
    print("filename" , filename)
    user_prompt = f"Por favor, forneça um resumo sucinto deste conteúdo:\n\n{content}"
    
    # Use Ollama to generate the summary with the specified model
    summary = get_ollama_response(model=model, system_prompt=system_prompt, user_prompt=user_prompt)
    
    # Check if the response is a dictionary, which indicates an error
    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n\n**Error**: {summary['error']}\n\n"
    
    # Ensure the summary is returned as a string and properly formatted
    formatted_summary = f"## Summary: {filename}\n\n{summary}\n---\n"
    
    # Return the formatted summary
    return formatted_summary

def summarize_with_ollama_final(content, filename, model):
    print('content: ', content)
    """
    create Readme using an Ollama model.
    """
    system_prompt = """
    você é um engenheiro de software que esta criando README.md para GitHub. resume os use o conhecimento que tem de outros projeto open source.
    Seja direto em suas respostas, não crie comentários. 
    Responda em formatado em Markdown, mas não use ```Markdown``` e Responda em Português (Br).
    Siga esta estrutura:
    **O que é o projeto**
    {'texto'}
    **Dependências**
    {'texto'}
    **Como instalar**
    {'texto'}
    **Como usar**
    {'texto'}
    """
    print("filename final" , filename)

    user_prompt = f"Faça usando este conteúdo:\n\{content}"
    
   
    summary = get_ollama_response(model=model, system_prompt=system_prompt, user_prompt=user_prompt)
    print('summary: ', summary);

    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n\n**Error**: {summary['error']}\n\n"   
    formatted_summary = f"## Summary: {filename}\n\n{summary}"
    return formatted_summary

def get_project_files(directory):
    """
    Recursively gets all files in the provided directory.
    """
    project_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.html', '.css', '.yml')):
                project_files.append(os.path.join(root, file))
    return project_files

def read_and_summarize_file(filepath, model):
    """
    Reads a file and returns its summary using the specified model.
    """
    filename = os.path.basename(filepath)
    if filepath.endswith('.txt'):
        with open(filepath, 'r') as file:
            content = file.read()
    elif filepath.endswith('.pdf'):
        with open(filepath, 'rb') as file:
            content = read_pdf(file)
    elif filepath.endswith('.docx'):
        with open(filepath, 'rb') as file:
            content = read_docx(file)
    else:
        with open(filepath, 'r') as file:
            content = file.read()    
    return summarize_with_ollama(content, filename, model)  
    

def generate_documentation(project_path, model):
    """
    Generates documentation by summarizing each file in the project directory with the selected model,
    ignoring files that match any pattern in ignore_files.
    """
    documentation = []
    project_files = get_project_files(project_path)
    
    # Patterns to ignore
    ignore_patterns = ["project_documentation.txt", "README.md", "*.pyc"]
    
    for file_path in project_files:
        file_name = os.path.basename(file_path)
        
        # Skip files that match any pattern in ignore_patterns
        if any(fnmatch.fnmatch(file_name, pattern) for pattern in ignore_patterns):
            continue

        summary = read_and_summarize_file(file_path, model)
        documentation.append(summary)
    
    return "\n".join(documentation)
