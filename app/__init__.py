from flask import Flask
from .secrets import secret_key
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:localhost:5432/store'
    #db = SQLAlchemy(app)
    db.init_app(app)
    

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
