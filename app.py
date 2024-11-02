from flask import Flask
from flasgger import Swagger
from config import Config
from src.routes.html_routes import html_routes
from src.routes.api_routes import api_routes

app = Flask(__name__, template_folder='src/templates' , static_folder='src/static')
app.config.from_object(Config)

Swagger(app)  # Initialize Swagger UI

# Register blueprints
app.register_blueprint(html_routes)
app.register_blueprint(api_routes)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
