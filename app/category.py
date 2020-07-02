from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)

    def __init__(self, name):
        self.name = name