from flask import Flask
from product import *

app = Flask('__name__')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:password@localhost:5432/store'

db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
