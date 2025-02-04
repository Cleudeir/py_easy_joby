import os
from Libs.LLM.Provider import send_image_to_gemini, send_image_to_ollama

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

system_prompt = "You are a software engineer.  will create documentation"
user_prompt = """
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
    
def describe_image_with_ollama(images_path: list[str]):    
    return send_image_to_gemini(system_prompt,user_prompt, images_path)
    
def describe_image_with_gemini(images_path: list[str]):
    return send_image_to_ollama(system_prompt,user_prompt, images_path)