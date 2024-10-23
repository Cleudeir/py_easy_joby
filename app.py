from flask import Flask, render_template, request
from modules.directory_structure import get_directory_structure
from modules.ollama import get_ollama_response, get_available_models  # Import the new function
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/directory_structure', methods=['GET', 'POST'])
def directory_structure():
    if request.method == 'POST':
        directory_path = request.form['directory_path']
        structure = get_directory_structure(directory_path)
        return render_template('directory_structure.html', structure=structure)
    return render_template('directory_structure.html')

@app.route('/ollama', methods=['GET', 'POST'])
def ollama():
    models = get_available_models()  # Fetch the available models
    if request.method == 'POST':
        model = request.form['model']
        system_prompt = request.form['system_prompt']
        user_prompt = request.form['user_prompt']
        
        # Get response from Ollama API
        response = get_ollama_response(model, system_prompt, user_prompt)
        return render_template('ollama.html', response=response, model=model, system_prompt=system_prompt, user_prompt=user_prompt, models=models)

    return render_template('ollama.html', models=models)  # Pass models to the template

if __name__ == "__main__":
    app.run(debug=True)
