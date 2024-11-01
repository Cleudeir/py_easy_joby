from flask import Flask
from flasgger import Swagger
from config import Config
from routes.html_routes import html_routes
from routes.api_routes import api_routes

app = Flask(__name__)
app.config.from_object(Config)

Swagger(app)  # Initialize Swagger UI

# Register blueprints
app.register_blueprint(html_routes)
app.register_blueprint(api_routes)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
