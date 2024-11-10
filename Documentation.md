# Summary: config.py

## Purpose of the Code

* This code defines a configuration class for a Flask application. It sets up various settings for the application, including the upload folder, debug mode, and Swagger configuration.

## Business Rule

* This code defines the configuration parameters necessary for the Flask application to function correctly. It sets the upload folder location, enables debug mode, and configures Swagger for API documentation. 

## List External Libraries

* No libraries used.

---

# Summary: requirements.txt

## Purpose of the Code

* The code likely involves web development, document processing, and potentially AI integration. 

##  Business Rule

* No business rule is mentioned.

## List external libraries


* **flask:** A popular Python framework for building web applications.
* **flasgger:** A library for automatically generating API documentation using Swagger.
* **pdfplumber:** A library for extracting text and tables from PDF documents.
* **python-docx:**  A library for creating and manipulating Microsoft Word documents.
* **ollama:** An open-source large language model framework.
* **markdown:** A lightweight markup language for creating formatted text.
* **google-generativeai:**  Google's generative AI library for tasks like text generation and image creation.
* **python-dotenv:** A library for loading environment variables from a `.env` file. 

---

# Summary: app.py

## Purpose of the Code

* This code creates a Flask application that serves both HTML routes and API endpoints. 

## Business Rule

* The code sets up the Flask application, loads configurations from the 'Config' object, initializes Swagger UI for documentation, and registers blueprints for HTML and API routes. 

## List external libraries

* `flask`: A Python framework for building web applications.
* `flasgger`: A Flask extension for generating API documentation with Swagger UI.
* `config`: A module containing configuration settings for the application.
* `src.routes.html_routes`: A module containing routes for HTML pages.
* `src.routes.api_routes`: A module containing routes for API endpoints. 

---

# Summary: directory_structure.html

## Purpose of the Code

* This code displays a web page that allows users to obtain the directory structure of a specified directory path.


##  Business rule

* The page either displays a form to input the directory path or displays the retrieved directory structure in a preformatted text block, depending on whether a valid path has been provided.

## List external libraries

* **Jinja2**: A templating engine used for rendering the HTML with dynamic content (e.g., displaying the directory structure).
* **Flask**: A Python web framework used to handle the routing and processing of user requests.

---

# Summary: index.html

## Purpose of the Code

* This code creates a simple HTML dashboard for a project manager application.

## Business Rule

* The dashboard presents a list of available modules, each with a link to a specific route.

## List External Libraries

* No libraries used. 

---

# Summary: ollama.html

## Purpose of the Code

* This code provides a web interface to interact with an Ollama model. Users can select a model, provide system and user prompts, and receive a response. The response is displayed in a preformatted area.

##  bussiness rule

* The code utilizes local storage to save the system prompt, selected model, and user prompt so that they persist across sessions.

## List external libraries

* No libraries used. 

---

# Summary: split_results.html

## Purpose of the Code


* This code is a webpage that displays the results of splitting a file by a given delimiter. 
##  bussiness rule

    
*  The code retrieves the sections of a file that were split by a specific text delimiter, and displays them in a list. 
## List external libraries


    * `url_for`: This is a function from the Flask framework for creating URLs.
    * `static`: This is a function from the Flask framework for serving static files.
    * `css/styles.css`: This is a stylesheet for styling the webpage. 

---

# Summary: project_documentation.html

## Purpose of the Code

* This code provides a web interface to generate documentation for projects. 
* Users can enter a project directory path and select a GPT provider and model to generate documentation. 

## Business Rule

* The code leverages external GPT providers to analyze the project's code and generate documentation. 
* It presents a user-friendly form for selecting project paths and providers. 

## List external libraries

* **Jinja2:** A templating language for generating dynamic HTML content.
* **Flask:** A lightweight web framework for creating web applications.
* **GPT Providers:** (Ollama, Gemini) -  These providers are external APIs that generate text based on given prompts.

---

# Summary: split_file.html

## Purpose of the Code

* This code implements a web form that allows users to upload a file and split it based on a chosen method.

##  bussiness rule

* The code provides three options for splitting: 
    * "Split by Text": Splits the file based on a user-provided text string.
    * "Split by Line Number": Splits the file based on a user-provided line number.
    * "Split by Paragraphs": Splits the file based on paragraph breaks.

## List external libraries

* No libraries used.

---

# Summary: api_routes.py

## Purpose of the Code

* The code defines a Flask Blueprint named `api_routes` that exposes several API endpoints for various tasks related to project documentation, directory structure analysis, file splitting, and interactions with the Ollama language model. 

## Business Rule

*  The code implements several business rules, including:
    * Generation of project documentation using a selected LLM model (Ollama) and GPT provider. 
    * Fetching the directory structure of a given directory path. 
    * Splitting files based on provided text, lines, or paragraphs.
    * Interacting with the Ollama language model to generate responses based on user prompts.
## List external libraries

* **Flask:** Framework for building web applications
* **flasgger:**  Used to generate Swagger documentation for APIs
* **os:**  Used for interacting with the operating system (e.g., creating directories)
* **jsonify:**  Flask extension for serializing Python data structures to JSON
* **request:** Flask extension for accessing incoming request data
* **current_app:** Flask object representing the current application
* **src.modules.directory_structure:**  Module containing functions related to directory structure analysis
* **src.modules.gpt:** Module containing functions for interacting with the Ollama language model
* **src.modules.file_processor:** Module containing functions for reading and splitting files
* **src.modules.project_documentation:** Module for generating project documentation. 

---

# Summary: html_routes.py

## Purpose of the Code

* The code is a Flask application that provides several functionalities related to file processing, documentation generation, and interaction with an LLM (Large Language Model) like Ollama.

## Business Rule

* The application allows users to upload files, split them into sections based on different criteria (text, lines, paragraphs), generate project documentation using an LLM, and summarize the documentation using the LLM. 
* It also provides functionality to interact with Ollama and get responses based on user prompts.

## List external libraries

* **Flask:**  A web framework for Python.
* **markdown:** A library for converting Markdown text to HTML.
* **os:** A Python module providing access to operating system functionalities.
* **src.modules.directory_structure:** A module containing functions to retrieve directory structure.
* **src.modules.gpt:** A module containing functions to interact with Ollama, including fetching available models and getting responses.
* **src.modules.file_processor:**  A module containing functions to read different file types (PDF, DOCX, TXT) and split them into sections.
* **src.modules.project_documentation:** A module containing functions to generate project documentation, summarize it using an LLM, and create LinkedIn posts based on the summary. 

---

# Summary: directory_structure.py

## Purpose of the Code

* The code generates a textual representation of the directory structure of a given path, excluding hidden directories (those starting with a dot).

## Business Rule

*  Ignore hidden directories, presenting only the structure of visible directories and their contained files.

## List external libraries

* `os`: This library provides functions for interacting with the operating system, including file and directory manipulation. 

---

# Summary: gpt.py

## Purpose of the Code

* The code provides functions for interacting with Google Generative AI (GenAI) and Ollama models. It enables sending user prompts and retrieving responses from both platforms. 

## Business Rule

*  The code is intended for applications requiring interaction with large language models (LLMs) like Google's Gemini and Ollama models. It provides flexibility in choosing the LLM based on the requirements of the application.
## List external libraries

* **google.generativeai as genai**: Google Generative AI library for interacting with Google's LLMs.
* **ollama**: Ollama library for communicating with Ollama's LLMs. 
* **os**: Python's operating system library for environment variable access. 

---

# Summary: project_documentation.py

## Purpose of the Code

* The code summarizes files in a project directory using a chosen language model (Ollama or Gemini). It generates documentation by creating summaries of individual files and saving them to a project documentation file.

## Business Rule

* The code is designed to automatically generate documentation for a project by summarizing the content of each file. The summaries are generated using an external LLM provider and are then combined into a single documentation file.

## List external libraries

* **os:** Provides functions for interacting with the operating system, including file operations.
* **time:** Provides time-related functions, including the sleep function used to introduce a delay between summaries.
* **src.modules.file_processor:**  Contains functions for reading PDF and DOCX files.
* **src.modules.gpt:** Contains functions for interacting with the selected LLM (Ollama or Gemini).
* **fnmatch:** Provides functions for Unix-style filename matching using patterns. 

---

# Summary: file_processor.py

## Purpose of the Code

* This code defines functions to read and split text from files, specifically PDF, DOCX and TXT files. 

## Business Rule

*  There are no explicit business rules defined in this code.

## List external libraries

* **pdfplumber:** Used for extracting text from PDF files while preserving formatting.
* **docx:**  Used for extracting text from DOCX files. 

---

# Summary: styles.css

## Purpose of the Code

* This code provides CSS styles for a web application. 

##  bussiness rule

* Not applicable.
## List external libraries

* No libraries used. 

---

# Summary: split_file.yml

## Purpose of the Code

* This code provides an API endpoint for splitting files into sections based on user-defined criteria.

## Business Rule

* Users can upload a file and choose a splitting method: "text" (split by a specific text pattern), "lines" (split by a specified number of lines), or "paragraphs". 
* The code processes the file and returns an array of file sections along with a description of the splitting method and value used.

## List external libraries

* No libraries used. 

---

# Summary: ollama.yml

## Purpose of the Code

* This code defines an API endpoint for generating responses using the Ollama AI model.
##  bussiness rule

* The API takes a user prompt and system-level prompt as input, selects an AI model, and uses Ollama to generate a response.
## List external libraries


* No libraries used. 

---

# Summary: directory_structure.yml

## Purpose of the Code

This code retrieves the structure of a directory given a path. 

## Business Rule

The code analyzes a given directory path and returns a nested dictionary structure representing the directory's contents. 

## List external libraries

* No libraries used. 

---

# Summary: get_project_documentation.yml

## Purpose of the Code

* The code defines an API endpoint for generating project documentation. 

##  bussiness rule

*  The API accepts a project path and a documentation model as input and generates a documentation string based on these parameters.

## List external libraries

* No libraries used. 

---
