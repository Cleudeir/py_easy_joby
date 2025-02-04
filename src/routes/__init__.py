from src.Modules.Home.route import home_routes
from src.Modules.reconstruction.route import reconstruction_routes
from src.Modules.project_documentation.route import project_documentation_routes
from src.Modules.file_splitter.route import file_splitter_routes
def register_blueprints(app):
    app.register_blueprint(home_routes)
    app.register_blueprint(reconstruction_routes)
    app.register_blueprint(project_documentation_routes)
    app.register_blueprint(file_splitter_routes)