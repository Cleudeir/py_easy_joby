from flask import Blueprint, render_template, request
from src.modules.gpt import get_ollama_models, get_ollama_response

ollama_response_routes = Blueprint('ollama_response_routes', __name__)

@ollama_response_routes.route('/ollama-response', methods=['GET', 'POST'])
def ollama_response():
    models = get_ollama_models()
    if request.method == 'POST':
        model = request.form['model']
        system_prompt = request.form['system_prompt']
        user_prompt = request.form['user_prompt']

        response = get_ollama_response(model, system_prompt, user_prompt)
        return render_template(
            'ollama.html',
            response=response,
            model=model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            models=models
        )
    return render_template('ollama.html', models=models)