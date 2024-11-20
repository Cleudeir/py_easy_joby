from flask import Flask
from config import Config
from src.routes import register_blueprints  # Import the blueprint registration function

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
app.config.from_object(Config)

# Register all blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
