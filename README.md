
## Project structure
```                    
easy_joby_py/
    README.md
    config.py
    requirements.txt
    app.py
    Documentation.md
    src/
        templates/
            agent_summary_reconstruction_code.html
            directory_structure.html
            index.html
            ollama.html
            error.html
            split_results.html
            project_documentation.html
            image_description.html
            refactor.html
            split_file.html
        routes/
            home.py
            directory_structure.py
            file_splitter.py
            agent_summary_reconstruction.py
            refactor.py
            project_documentation.py
            image_description.py
            ollama_response.py
        modules/
            agent_summary_reconstruction_code.py
            directory_structure.py
            refactor.py
            gpt.py
            project_documentation.py
            image_description.py
            file_processor.py
        static/
            images/                
            css/
                styles.css                
```
## Descrição do Projeto

Este projeto é uma aplicação web para gerenciamento de projetos, oferecendo diversas ferramentas para otimizar o processo de desenvolvimento.  Ele inclui funcionalidades para: obter estrutura de diretórios, interagir com sistemas externos, dividir arquivos, refatorar código, gerar documentação de imagens, reconstrução de resumos de agentes e gerar documentação de projetos.  Utiliza modelos de linguagem grandes (LLMs) como Ollama e Gemini para auxiliar na geração de documentação.

## Dependências

Antes de usar este projeto, instale as dependências:

```
flask
pdfplumber
scikit-learn
jinja2
pytesseract
torch
torchvision
pillow
opencv-python
flasgger
python-docx
ollama
google-generativeai
markdown
python-dotenv
pypandoc
```

## Como Instalar

1. Clone este repositório.
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env` com as configurações necessárias (chave de API do Google Generative AI, etc.).
4. Execute a aplicação: `python app.py` (ou comando apropriado para o seu ambiente de desenvolvimento).

## Como Usar

A aplicação web fornece uma interface para acessar diferentes módulos. Cada módulo oferece funcionalidades específicas:

* **Estrutura de diretórios:** Exibe a estrutura de arquivos e pastas de um diretório especificado.
* **Divisão de arquivos:** Permite dividir arquivos grandes em partes menores, com base em diferentes critérios (texto, número de linhas, parágrafos).
* **Refatoração de código:** Ajuda a refatorar código, separando-o em funções.
* **Documentação de imagens:** Gera documentação descritiva para imagens, utilizando modelos de linguagem.
* **Reconstrução de resumos de agentes:** Reconstrói o código baseado em um resumo gerado por um modelo de linguagem.
* **Documentação de projetos:** Gera uma documentação completa para um projeto, incluindo resumos de arquivos, sumário geral e post para o LinkedIn.
* **Interface Ollama:** Permite interação com modelos Ollama.


## Arquitetura

A aplicação é baseada em Flask, utilizando blueprints para organizar as rotas.  Os módulos individuais (estrutura de diretórios, divisão de arquivos, etc.) são implementados como blueprints separados, melhorando a organização e manutenibilidade do código. A geração de documentação se baseia fortemente em modelos de linguagem grandes acessados através de APIs (Ollama e Google Generative AI).


## Pipeline

O pipeline geral envolve:

1. **Solicitação do Usuário:** O usuário interage com a aplicação web via formulários.
2. **Processamento:** A aplicação processa a solicitação do usuário, possivelmente utilizando modelos de linguagem para gerar documentação ou realizar outras tarefas.
3. **Geração de Saída:** A aplicação gera a saída, que pode ser um HTML, um arquivo de texto ou outro formato, dependendo da funcionalidade.
4. **Exibição da Saída:** A saída é exibida ao usuário na interface web.

A arquitetura modular permite que cada funcionalidade tenha seu próprio pipeline específico, mas seguindo o fluxo geral descrito acima.
                
                