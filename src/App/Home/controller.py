from flask import Blueprint, render_template

home_routes = Blueprint('home_routes', __name__, template_folder='.')

@home_routes.route('/')
def home():
    """Home Page"""
    return render_template('view_home.html')
