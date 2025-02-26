from flask import Flask
from dotenv import load_dotenv
from src.App import register_blueprints
from config import Config

load_dotenv(dotenv_path='.env', override=True, verbose=True)

app = Flask(__name__, template_folder='src/templates', static_folder='src')
app.config.from_object(Config)

# Register all blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
