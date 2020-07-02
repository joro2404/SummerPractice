from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    statusCode = db.Column(db.String(10), unique=False)
    status = db.Column(db.String(128), unique=False)

    def __init__(self, statusCode, status):
        self.statusCode = statusCode
        self.status = status