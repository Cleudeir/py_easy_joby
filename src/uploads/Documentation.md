# Summary: directory_structure.html

## Purpose of the Code


* This code implements a web page that retrieves and displays the directory structure of a given path.
## Core Logic

* The code renders an HTML form that allows users to input an absolute directory path.
* Upon submission, the code uses Flask's routing mechanism to process the request and retrieve the directory structure.
* The retrieved structure is then presented to the user in a preformatted text block.
* If no path is provided, the page displays a form for user input.
## List external libraries

* **Flask:** A web framework for Python.
* **Jinja2:** A templating engine used for rendering the HTML content.
* **OS:** Built-in Python library for interacting with the operating system.
* **CSS:** Used to style the elements of the webpage. 

---

# Summary: index.html

## Purpose of the Code

* This HTML code creates a dashboard for a project management tool. It displays a list of available modules, each linked to a specific functionality. 

## Core Logic

* The code defines the basic structure of the dashboard, including a title, a heading for available modules, and an unordered list of links to various modules. Each link points to a specific route defined in the Flask application using `url_for`.

## List external libraries

* No libraries used. 

---

# Summary: ollama.html

## Purpose of the Code

* The code presents a web interface for interacting with an Ollama language model. Users can input a system prompt, a user prompt, and select a model to generate a response.

## Core Logic

* The code handles the following:
    * Displays a dropdown menu to select an Ollama model.
    * Allows users to input a system prompt and a user prompt.
    * Submits the prompts and selected model to a server-side endpoint.
    * Displays the generated response from the Ollama model.
    * Saves user input to local storage for persistence.
    * Shows a loading indicator while the model generates the response.

## List external libraries

* No libraries used. 

---

# Summary: split_results.html

## Purpose of the Code

* This HTML code displays the results of a file splitting process. It presents a list of sections extracted from the original file, based on a specified splitting criteria. 

## Core Logic

* The code uses Jinja templating to dynamically generate the HTML content.
* It iterates through a list of "sections" provided from a backend process.
* Each section is displayed as a preformatted text block within an unordered list. 
* A link is included to navigate back to the file splitting tool.

## List external libraries 

* No libraries used. 

---

# Summary: project_documentation.html

## Purpose of the Code

* This code implements a web application that generates documentation for a project. It allows users to input a project directory path, select a GPT provider and model, and generate documentation using the selected provider. 


## Core Logic

* The code renders a form that prompts the user for a project path, GPT provider, and model.
* Upon form submission, the user's input is processed to generate documentation using the selected GPT provider and model.
* The generated documentation is displayed within a Markdown-formatted section. 
* The code includes a loading overlay to indicate that the documentation generation process is in progress.

## List external libraries 

* No libraries used. 

---

# Summary: split_file.html

## Purpose of the Code

* This code creates a web page for uploading a file and splitting it based on different methods.

## Core Logic

* The code utilizes HTML for the user interface and JavaScript for dynamic functionality.
* Users upload a file (PDF, DOCX, or TXT) and choose a splitting method: split by text, split by line number, or split by paragraphs.
* For "Split by Text" and "Split by Line Number" methods, an input field appears to provide the text or line number for splitting.
* The code sends the file and chosen parameters to a backend server for file processing.
* A link provides navigation to the "Dashboard" upon completion.

## List external libraries

* No libraries used. 

---

# Summary: api_routes.py

## Purpose of the Code

* The code defines API endpoints for handling various file-related operations, including project documentation generation, directory structure retrieval, file splitting, and interactions with LLM models.

## Core Logic

* The code defines four API routes:
    * `/api/get-project-documentation`: Generates documentation for a given project based on user-selected LLM model.
    * `/api/directory-structure`: Returns the directory structure of a specified path.
    * `/api/ollama`: Sends a user prompt to an LLM model and returns the response.
    * `/api/file-splitter`: Splits a file into sections based on different methods (text, lines, paragraphs).

* The code utilizes libraries and functions for:
    * Reading and processing various file types (PDF, DOCX, TXT).
    * Generating project documentation using LLMs.
    * Obtaining directory structure information.
    * Communicating with LLM models.

## List external libraries

* **Flask**: A web framework for building web applications.
* **flasgger**: A library for generating Swagger documentation for Flask APIs.
* **os**: Provides functions for interacting with the operating system. 
* **src.modules.directory_structure**: Provides functions for retrieving directory structure.
* **src.modules.gpt**: Provides functions for interacting with LLM models, including `get_ollama_response` and `get_ollama_models`.
* **src.modules.file_processor**: Provides functions for reading and splitting files.
* **src.modules.project_documentation**: Provides functions for generating project documentation.


---

# Summary: html_routes.py

## Purpose of the Code

The code implements a web application that provides functionalities for generating documentation from project directories, interacting with a large language model (LLM) via Ollama, splitting files into sections based on various criteria, and displaying directory structures.

## Core Logic

* **Home Page:** Displays a basic home page.
* **Project Documentation:** 
    * Allows users to input a project directory path.
    * Extracts information from the project directory.
    * Uses a selected LLM model to generate documentation for the project.
    * Saves generated documentation to a file.
    * Summarizes the documentation.
* **Directory Structure:** 
    * Allows users to input a directory path.
    * Displays the directory structure in a hierarchical format.
* **Ollama Interaction:** 
    * Provides a user interface to interact with the Ollama LLM.
    * Allows users to select a model, input system and user prompts, and receive responses.
* **File Splitter:** 
    * Allows users to upload a file (PDF, DOCX, or TXT).
    * Splits the file into sections based on provided criteria (text, lines, or paragraphs).

## List External Libraries

* **Flask:** Web framework for building web applications.
* **markdown:**  Library for converting Markdown text to HTML.
* **os:** Provides functions for interacting with the operating system.
* **src.modules.directory_structure:** Provides functionality to get the directory structure of a given path.
* **src.modules.gpt:**  Provides functionality to interact with Ollama LLM.
* **src.modules.file_processor:** Provides functionality to read and split files based on different criteria.
* **src.modules.project_documentation:** Provides functionality to generate documentation for a project and summarize it. 

---

# Summary: directory_structure.py

## Purpose of the Code

* This Python code generates a structured representation of a directory's contents. 
## Core Logic

* The function `get_directory_structure` takes a directory path as input.
* It iterates through the directory using `os.walk` to traverse subdirectories and files.
* The code constructs a nested list representing the directory structure, with indentation based on the directory depth.
*  It filters out hidden directories (those starting with '.') and returns the structured representation as a string.
## List external libraries

* `os`: Used for file system interactions, including checking if a directory exists and traversing directory structures. 

---

# Summary: gpt.py

## Purpose of the Code

* The code provides functions to get responses from Google Generative AI (GenAI) and Ollama using specified prompts. 

## Core Logic

* The code defines two functions: `get_genai_response` and `get_ollama_response`. 
* `get_genai_response` takes system and user prompts as input and uses the Google Generative AI API to generate a response based on these prompts.
* `get_ollama_response` takes a model name, system, and user prompt as input and uses the Ollama API to get a response from the specified Ollama model using the given prompts.

## List external libraries

* `os`: for environment variables. 
* `ollama`: for interacting with Ollama models.
* `google.generativeai`: for interacting with Google Generative AI. 

---

# Summary: project_documentation.py

## Purpose of the Code

* The code's purpose is to automatically generate documentation for a software project by summarizing the content of each file in the project directory using a large language model (LLM).

## Core Logic

* The code utilizes the Ollama and Gemini LLMs to generate summaries of files with different formats like text, PDF, and DOCX.
* It allows users to choose between the Ollama and Gemini models and provides the ability to customize the system prompt.
* The code includes functions to read and summarize files, generate documentation, and recursively get all files from a directory.
* It utilizes the `fnmatch` library to ignore specific file patterns, such as `.pyc` files, and creates a delay between summaries to avoid rate limiting.

## List external libraries

* `os`: for interacting with the operating system, including file system operations.
* `time`: for handling time-related operations, such as delaying summaries.
* `src.modules.file_processor`: for reading PDF and DOCX files.
* `src.modules.gpt`: for interacting with the Ollama and Gemini LLMs.
* `fnmatch`: for pattern matching of file names. 

---

# Summary: file_processor.py

## Purpose of the Code

* This code provides functions to read and split the content of various file types (PDF, DOCX, and TXT). It allows users to split the content by text, lines, or paragraphs.

## Core Logic

* The code offers functions for reading different file types (PDF, DOCX, TXT) and extracting their text content.
* It includes functions for splitting the extracted text based on user-defined criteria:
    * `split_file_by_text`: Splits the text based on a specific delimiter text.
    * `split_file_by_lines`: Splits the text into sections with a specified number of lines per section.
    * `split_file_by_paragraphs`: Splits the text into individual paragraphs.
## List external libraries

* `pdfplumber`: Library for extracting text from PDF files with layout preservation.
* `docx`: Library for working with DOCX files, allowing text extraction. 

---

# Summary: styles.css

## Purpose of the Code

* This CSS code defines styles for a webpage, providing a consistent visual appearance and enhancing user experience.

## Core Logic

* **Basic Styles:** The code sets default styles for the body, headings, links, and form elements, establishing a clean and modern aesthetic. 
* **Containers:** A `container` class is defined for centering content and applying consistent padding and borders.
* **Form Elements:** Specific styles are applied to labels, input fields, textareas, buttons, and select elements, ensuring proper display and user interaction. 
* **Loading Indicator:** A loading spinner animation is implemented, visually indicating ongoing processes to the user. 
* **Markdown Content:** Styles are defined to format Markdown content within the webpage, enhancing readability and code display.
* **Responsive Design:** Media queries are included to adapt the layout and font sizes for different screen sizes, providing optimal viewing on various devices. 

## List External Libraries

* No libraries used. 

---

# Summary: split_file.yml

## Purpose of the Code

This code defines an API endpoint for splitting an uploaded file into sections based on user-specified criteria.

## Core Logic

The endpoint receives a file, the splitting method (text, lines, or paragraphs), and an optional split value.  It then processes the file and splits it according to the chosen method. The endpoint returns an array of file sections and a description of the split method used.

## List external libraries

* No libraries used. 

---

# Summary: ollama.yml

## Purpose of the Code

* This code defines an API endpoint for generating responses using the Ollama model.

## Core Logic

* The endpoint accepts three parameters: `model`, `system_prompt`, and `user_prompt`.
* It uses the specified AI model (`model`) to generate a response based on the provided system and user prompts.
* The generated response is returned as a JSON object with the `response` field containing the text output.

## List external libraries

* No libraries used. 

---

# Summary: directory_structure.yml

## Purpose of the Code

This code defines an API endpoint for retrieving the directory structure of a given path. 

## Core Logic

The endpoint accepts a directory path as input. It then processes this path and returns a nested dictionary structure representing the directory's contents. If the provided path is invalid, a 400 error is returned.

## List external libraries

* No libraries used. 

---

# Summary: get_project_documentation.yml

## Purpose of the Code

* This code defines an API endpoint for generating project documentation. The API accepts a project directory path and a selected model to produce documentation.

## Core Logic

* The API endpoint accepts a POST request with the project path and model name as parameters.
* It processes the request, generates documentation based on the provided information, and returns the documentation content in the response.
* It handles potential errors, returning appropriate error messages for invalid input or server issues.

## List external libraries

* No libraries used. 

---

# Summary: Documentation.md

## Purpose of the Code


* This CSS code styles a web application, focusing on visual appeal and user experience.
## Core Logic

* The code uses CSS selectors to style different HTML elements.
* It employs properties like `font-family`, `color`, `margin`, etc. to control element appearance.
* Media queries ensure responsiveness across screen sizes.
* Styles are included for markdown content and a loading spinner.
## List external libraries


* No libraries used. 

---
