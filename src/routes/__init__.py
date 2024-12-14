from .receive_files import receive_files_routes
from .home import home_routes
from .image_description import image_description_routes
from .refactor import refactor_routes
from .agent_summary_reconstruction import agent_summary_reconstruction_routes
from .project_documentation import project_documentation_routes
from .directory_structure import directory_structure_routes
from .ollama_response import ollama_response_routes
from .file_splitter import file_splitter_routes


def register_blueprints(app):
    app.register_blueprint(home_routes)
    app.register_blueprint(image_description_routes)
    app.register_blueprint(refactor_routes)
    app.register_blueprint(agent_summary_reconstruction_routes)
    app.register_blueprint(project_documentation_routes)
    app.register_blueprint(directory_structure_routes)
    app.register_blueprint(ollama_response_routes)
    app.register_blueprint(file_splitter_routes)
    app.register_blueprint(receive_files_routes)
