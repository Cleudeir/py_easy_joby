
                # file_processor.py                
                ## project structure
                ```                    
                py_easy_joby/
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
            concatenate_project.py
            agent_summary_reconstruction_code.py
            directory_structure.py
            refactor.py
            gpt.py
            project_documentation.py
            image_description.py
            file_processor.py
        static/
            css/
                styles.css                
                ```
                ## Propósito e Descrição do Projeto

Este projeto fornece uma biblioteca reutilizável para processamento de arquivos de texto, focando na extração de texto de PDFs, DOCX e TXT, e na divisão flexível desse texto em seções menores.  É útil para análise de texto, extração de dados e organização de documentos.

## Dependências

Antes de usar este projeto, instale as dependências:

```
pdfplumber
python-docx
```

## Como Instalar

1. Clone este repositório.
2. Instale as dependências: `pip install -r requirements.txt`

## Como Usar

1. Importe as funções necessárias de `file_processor.py`.
2. Use `read_pdf`, `read_docx`, ou `read_txt` para extrair texto de um arquivo.
3. Utilize `split_file_by_text`, `split_file_by_lines`, ou `split_file_by_paragraphs` para dividir o texto conforme necessário.


## Arquitetura

O script é modular, separando a leitura de arquivos e a divisão de texto em funções distintas.  Isso melhora a legibilidade, manutenção e reusabilidade do código.

## Pipeline

1. **Leitura de Arquivo:** O tipo de arquivo é identificado e a função apropriada (`read_pdf`, `read_docx`, `read_txt`) é usada para extrair o texto.
2. **Divisão de Texto:** O texto é dividido usando uma das funções de divisão, dependendo do critério escolhido pelo usuário.
3. **Saída:** Uma lista de strings (cada string representando uma seção do texto) é retornada.


                
                