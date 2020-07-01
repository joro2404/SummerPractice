from flask import Flask
from .secrets import secret_key

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = secret_key

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
