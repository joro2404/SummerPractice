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
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    phone_number = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=True)

    def __init__(self, id, name, email, password, is_admin, is_confirmed, phone_number, address):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_confirmed= is_confirmed
        self.phone_number = phone_number 
        self.address = address


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Subcategory(db.Model):
    __tablename__ = "subcategories"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)
    subcategory = db.Column(db.Text, nullable=False)

    def __init__(self, id, category_id, subcategory):
        self.id = id
        self.category_id = category_id
        self.subcategory = subcategory


class Status(db.Model):
    __tablename__ = "status"
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, id, status):
        self.id = id
        self.status = status


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    price = db.Column(db.Float(5, 2), nullable=False)
    brand_id = db.Column(db.Integer, ForeignKey('brands.id'), nullable=False)
    overallRaiting = db.Column(db.Float(1, 2), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)
    gender = db.Column(db.Text, nullable=False)

    def __init__(self, id, name, price, brand_id, overallRaiting, category_id, gender):
        self.id = id
        self.name = name
        self.price = price
        self.brand_id = brand_id
        self.overallRaiting = overallRaiting
        self.category_id = category_id
        self.gender = gender


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    status_id = db.Column(db.Integer, ForeignKey('status.id'), nullable=False)
    payment_method_id = db.Column(db.Integer, ForeignKey('paymentMethods.id'), nullable=False)
    is_paid = db.Column(db.Boolean, nullable=False)
    phone_number = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)

    def __init__(self, id, date, user_id, product_id, status_id, payment_method_id, is_paid, phone_number, address):
        self.id = id
        self.date = date
        self.user_id = user_id
        self.product_id = product_id
        self.status_id = 
        self.payment_method_id = payment_method_id
        self.is_paid = is_paid
        self.phone_number = phone_number
        self.address = address


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

    def __init__(self, id, product_id, path):
        self.id = id
        self.product_id = product_id
        self.path = path


class Size(db.Model):
    __tablename__ = "sizes"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    size = db.Column(db.Text, nullable=False)
    available = db.Column(db.Integer, nullable=False)

    def __init__(self, id, product_id, size, available):
        self.id = id
        self.product_id = product_id
        self.size = size
        self.available = available


class OrderedProduct(db.Model):
    __tablename__ = "orderedProducts"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)

    def __init__(self, id, order_id, product_id):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id



class PaymentMethod(db.Model):
    __tablename__ = "paymentMethods"

    id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.Text, nullable=False)

    def __init__(self, id, payment_method):
        self.id = id
        self.payment_method = payment_method