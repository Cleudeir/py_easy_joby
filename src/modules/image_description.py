import os
import ollama
import google.generativeai as genai
from src.modules.gpt import get_genai_response, get_ollama_response  # M

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


prompt_image_documents = """
    Analise as Imagens e Ajude a Documentar o Software, flow structure, no comments, no explanation.
    
    ## Nome da tela
    * Nome
    
    ## Descrição da tela
    * breve descrição da tela
    
    (Se existir busca e/ou filtro)
    ## Campos input busca e/ou filtro:
    Formato de Tabela com campos com a estrutura:
    “Nome,Tipo,Validação,Observação”
    
    (Se existir cartão com indicadores)
        ## Cartões com Indicadores:
        Formato de Tabela com campos com a estrutura:
        “Nome,Tipo,Validação,Observação”
    
    Se existir gráfico
        ## Gráficos:
        Formato de Tabela com campos com a estrutura:
        “Nome,Tipo,Eixo X (nome e unidade),Eixo Y(nome e unidade),”
        Se existir rádios no gráfico, adicionar subtítulo "variações" listando em formato de lista todas as opções e explique a função..

    Se existir lista
        ## Lista:
        Formato de Tabela com campos com a estrutura:
        “Nome, Tipo, Validação, Observação”
        se a lista tiver como resultado  "Nenhum registro foi encontrado ...", adicione um texto: "O sistema não apresenta nenhum dado registrado, o que torna insuficientes as informações para a descrição deste item. Dados adicionais serão incluídos nos próximos relatórios de detalhamento."
        
    Se existir formulário
        ## Formulário : 
        ### nome do fomulário
        Formato de Tabela com campos com a estrutura:
        “Nome, Tipo, Validação, Observação”
        Se existem campos com o ícone de cadeado, adicione abaixo da tabela o subtitulo:         
            ### Observação :
            * Os campos com o ícone de cadeado permitem que o valor seja travado para reutilização em futuras transferências, facilitando o preenchimento para valores que são 
            frequentemente reutilizados."
    
    ## Regra de Negócio:
    * Lógica de Processamento: crie usando a imagem como referência,
    * Ações Condicionais: crie usando a imagem como referência,
    
    
    Regras criação do relatório:       
    - Verifique se exite elemento semelhante a estrutura se existir adicione no relatório.
    - Sempre crie a regra de negócio.
    - Não adicione comentários, apenas títulos e subtítulos quando necessário.
    - Não use traços ou linhas como separador entre os parágrafos.
    - se campo for vazio, adicione a informação: “-”
    - se o tipo de item não existir, não o adicione.
    - create using markdown format.
    - responda em português.
    """
    
def describe_image_with_ollama(image_path):
    """
    Uses Ollama Vision to describe an image.
    
    Args:
        model_name (str): The name of the Ollama model to use.
        image_path (str): Path to the image file.
        user_prompt (str): The user prompt for the description.

    Returns:
        str: The description provided by the Ollama model.
    """
   
    try:
        # Send the user message and image to the Ollama Vision model
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': prompt_image_documents,
                'images': [image_path]
            }]
        )
        # Extract and return the content of the response
        return response.get('message', {}).get('content', 'No description available')
    except Exception as e:
        return f"Error describing image {image_path}: {str(e)}"
    
def describe_image_with_gemini(image_path):
    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )
    
    file = genai.upload_file(image_path)
    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            file,  
            prompt_image_documents          
        ],
        },       
    ]
    )
    response = chat_session.send_message('create')
    print(response.text)
    return response.text