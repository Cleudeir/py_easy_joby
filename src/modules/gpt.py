import os
import ollama
import google.generativeai as genai  # M

# Function to get a response from Google Generative AI with model, system, and user prompts
def get_genai_response(system_prompt, user_prompt):
    try:   
        model_name = "gemini-1.5-flash"
        # Configure the API key
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        # Define the generation configuration
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        # Create the generative model with the specified configuration and system instruction
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_prompt,
        )
        
        # Start a chat session
        chat_session = model.start_chat(history=[])
        
        # Send the user prompt and return the response
        response = chat_session.send_message(user_prompt)
        return response.text
    except Exception as e:
        return {"error": str(e)}


# Function to get available models from Ollama
def get_ollama_models():
    try:
        # Fetch available models using ollama.list
        response = ollama.list()
        models = response.get('models', [])  # Extract models from the response
        model_names = [model['name'] for model in models]  # Get the model names
        return model_names
    except Exception as e:
        return {"error": str(e)}

# Function to get a response from an Ollama model
def get_ollama_response(model_name, system_prompt, user_prompt):
    try:
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]        
        # Call ollama.chat with the specified model and messages
        response = ollama.chat(model=model_name, messages=messages)
        # Return the response content directly
        response_message = response['message']['content']
        return response_message
    except Exception as e:
        return {"error": str(e)}

# Function to get embeddings from an Ollama model
def get_ollama_embeddings(model_name, text_input):
    try:
        # Call ollama.embedding with the specified model and input text
        response = ollama.embed(model=model_name, input=text_input)
        # Extract and return the embeddings
        embeddings = response['embeddings']
        return embeddings
    except Exception as e:
        return {"error": str(e)}

user_prompt = """
    Analise as Imagens e Ajude a Documentar o Software, flow structure, no comments, no explanation.
    
    # Nome da tela
    
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
    
    (Se existir gráfico)
    ## Gráficos:
    Formato de Tabela com campos com a estrutura:
    “Nome,Tipo,Eixo X,Eixo Y”
    Se existir rádios no gráfico, adicionar subtítulo "variações" listando em formato de lista todas as opções e explique a função..
    
    (Se existir lista)
    ## Lista:
    Formato de Tabela com campos com a estrutura:
    “Nome, Tipo, Validação, Observação”
    se a lista tiver como resultado  "Nenhum registro foi encontrado ...", adicione um texto: "O sistema não apresenta nenhum dado registrado, o que torna insuficientes as informações para a descrição deste item. Dados adicionais serão incluídos nos próximos relatórios de detalhamento."
    
    (Se existir formulário)
    ## Formulário : 
    ### nome do fomulário
    Formato de Tabela com campos com a estrutura:
    “Nome, Tipo, Validação, Observação”
    if existem campos com o ícone de cadeado, adicione abaixo da tabela o subtitulo:         
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
                'content': user_prompt,
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
            user_prompt          
        ],
        },       
    ]
    )
    response = chat_session.send_message('create')
    print(response.text)
    return response.text