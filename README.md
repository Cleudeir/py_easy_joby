## Project structure:

* **app.py:** Main Flask application file.
* **config.py:** Configuration settings for the Flask app.
* **requirements.txt:** List of project dependencies.
* **src:**
    * **routes:**
        * **api_routes.py:** API endpoints for the application.
        * **html_routes.py:** Routes for HTML pages.
    * **modules:**
        * **directory_structure.py:** Functions for retrieving directory structure.
        * **gpt.py:** Functions for interacting with Google Generative AI and Ollama.
        * **file_processor.py:** Functions for reading and splitting files.
        * **project_documentation.py:** Functions for generating project documentation.
* **templates:**
    * **directory_structure.html:** Template for displaying directory structure.
    * **index.html:** Main dashboard template.
    * **ollama.html:** Template for interacting with Ollama.
    * **split_results.html:** Template for displaying split file results.
    * **project_documentation.html:** Template for generating project documentation.
    * **split_file.html:** Template for splitting files.
    * **styles.css:** CSS styles for the application.

## Project description

This project is a Flask web application providing various functionalities related to file processing, documentation generation, and interaction with large language models (LLMs). 

## Dependencies

Before you can start using or working with this project, make sure to install the following dependencies:

```
flask
flasgger
pdfplumber
python-docx
ollama
markdown
google-generativeai
python-dotenv
```

## How to Install

To get this project up and running, follow these steps:

1. **Clone the repository:** `git clone <repository URL>`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Create a .env file:**
    * `FLASK_APP=app.py`
    * `FLASK_ENV=development`
    * `UPLOAD_FOLDER=uploads`
    * (Optional) API keys for Google Generative AI and Ollama.
4. **Run the application:** `flask run`

## How to Use

Once you have the project set up, you can start using it in the following ways:

* **Browse the HTML routes:** Access the various pages through the provided URLs.
* **Use the API endpoints:** Use tools like Postman or curl to interact with the API endpoints.
* **Explore the documentation:** Utilize the Swagger UI for exploring available API endpoints.
* **Customize the application:** Modify the code to suit your specific needs.
