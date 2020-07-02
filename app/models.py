from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    phone_number = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=True)

    def __init__(self, id, name, email, password, is_admin, phone_number, address):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.phone_number = phone_number 
        self.address = address


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Status(db.Model):
    __tablename__ = "status"
    
    id = db.Column(db.Integer, primary_key=True)
    statusCode = db.Column(db.String(10), unique=True, nullable=False)
    status = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, id, statusCode, status):
        self.id = id
        self.statusCode = statusCode
        self.status = status


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    price = db.Column(db.Float(5, 2), nullable=False)
    available = db.Column(db.Integer, nullable=False)
    overallRaiting = db.Column(db.Float(1, 2), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)
    #category = relationship('categories', back_populates="products")

    def __init__(self, id, name, price, available, overallRaiting, category_id):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.overallRaiting = overallRaiting
        self.category_id = category_id


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    status = db.Column(db.String(3), ForeignKey('status.statusCode'), nullable=False)

    def __init__(self, id, date, user_id, product_id, status):
        self.id = id
        self.date = date
        self.user_id = user_id
        self.product_id = product_id
        self.status = status


class Raiting(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    raiting = db.Column(db.Integer, nullable=False)

    def __init__(self, id, user_id, product_id, raiting):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.raiting = raiting


class Favourite(db.Model):
    __tablename__ = "favourites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)

    def __init__(self, id, user_id, product_id):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id

class Picture(db.Model):
    __tablename__ = "pictures"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    path = db.Column(db.Text, nullable=False) 