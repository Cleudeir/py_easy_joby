from src.App.Home.controller import home_routes
from src.App.reconstruction.route import reconstruction_routes
from src.App.project_documentation.controller import project_documentation_routes
from src.App.file_splitter.controller import file_splitter_routes
from src.App.directory_structure.controller import directory_structure_routes
def register_blueprints(app):
    app.register_blueprint(home_routes)
    app.register_blueprint(reconstruction_routes)
    app.register_blueprint(project_documentation_routes)
    app.register_blueprint(file_splitter_routes)
    app.register_blueprint(directory_structure_routes)