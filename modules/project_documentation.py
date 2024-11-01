import os
from modules.file_processor import read_txt, read_pdf, read_docx
from modules.ollama import get_ollama_response

def summarize_with_ollama(content, filename, model):
    """
    Summarizes the content of a file using an Ollama model and returns it in Markdown format,.
    """
    system_prompt = """
    Você é um assistente útil que resume arquivos. Seja direto em suas respostas, não crie comentários. Responda em formatado em Markdown, mas não use ```Markdown``` e Responda em Português (Br). Use a estrutura:

    - **Objetivo do Código**: Descrição breve da finalidade do arquivo de código.

    - **Lógica Central e Algoritmos**:
    - Resumo dos principais algoritmos ou lógica implementada.

    - **Dependências e Bibliotecas**:
    - Mencionar bibliotecas ou frameworks externos usados.

    - **Entrada e Saída**:
    - Descrição das entradas aceitas e saídas produzidas pelo código.

    - **Tratamento de Erros e Exceções**:
    - Como o código lida com erros ou exceções.

    - **Considerações de Segurança**:
    - Pontuar características de segurança ou vulnerabilidades potenciais, sem código.

    - **Configuração e Ambiente**:
    - Descrição de quaisquer arquivos de configuração ou variáveis de ambiente necessárias.

    - **Testes e Validação**:
    - Informações sobre testes unitários ou de integração fornecidos.

    Se o arquivo não se tratar de código, faça apenas o resumo.
    """

    user_prompt = f"Por favor, forneça um resumo sucinto deste conteúdo:\n\n{content}"
    
    # Use Ollama to generate the summary with the specified model
    summary = get_ollama_response(model=model, system_prompt=system_prompt, user_prompt=user_prompt)
    
    # Check if the response is a dictionary, which indicates an error
    if isinstance(summary, dict) and "error" in summary:
        return f"**{filename} Summary**\n\n**Error**: {summary['error']}\n\n"
    
    # Ensure the summary is returned as a string and properly formatted
    formatted_summary = f"## Summary: {filename}\n\n{summary}"
    
    # Return the formatted summary
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
    Generates documentation by summarizing each file in the project directory with the selected model.
    """
    documentation = []
    project_files = get_project_files(project_path)
    
    for file_path in project_files:
        summary = read_and_summarize_file(file_path, model)
        documentation.append(summary)
    
    return "\n".join(documentation)

def save_documentation(output_path, content):
    """
    Saves the generated documentation to a specified output file.
    """
    with open(output_path, 'w') as doc_file:
        doc_file.write(content)
