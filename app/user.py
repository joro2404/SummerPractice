from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    phone_number = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=True)


    def __init__(self, name, email, password, admin, phone_number, address):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin
        self.phone_number = phone_number 
        self.address = address