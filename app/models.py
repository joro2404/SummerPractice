from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    phone_number = db.Column(db.Text, nullable=True)

    def __init__(self, id, username, first_name, last_name, email, password, is_admin, is_confirmed, phone_number):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed
        self.phone_number = phone_number 


class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    receiver_name = db.Column(db.Text, nullable=False)
    receiver_phone = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)

    def __init__(self, id, user_id, receiver_name, receiver_phone, address):
        self.id = id
        self.user_id = user_id
        self.receiver_name = receiver_name
        self.receiver_phone = receiver_phone
        self.address = address


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, id, tag):
        self.id = id
        self.tag = tag


class ProductTags(db.Model):
    __tablename__ = "products_tags"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    tag_id = db.Column(db.Integer, ForeignKey('tags.id'), nullable=False)

    def __init__(self, id, product_id, tag_id):
        self.id = id
        self.product_id = product_id
        self.tag_id = tag_id


class Status(db.Model):
    __tablename__ = "status"
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, id, status):
        self.id = id
        self.status = status


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    brand_id = db.Column(db.Integer, ForeignKey('brands.id'), nullable=False)
    overall_rating = db.Column(db.Float(1, 2), nullable=False)
    gender_id = db.Column(db.Integer, ForeignKey('genders.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = 0

    def __init__(self, id, name, price, brand_id, overall_rating, gender, description):
        self.id = id
        self.name = name
        self.price = price
        self.brand_id = brand_id
        self.overall_rating = overall_rating
        self.gender_id = gender
        self.description = description


class Gender(db.Model):
    __tablename__ = "genders"

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text, nullable=False)

    def __init__(self, id, gender):
        self.id = id
        self.gender = gender


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    status_id = db.Column(db.Integer, ForeignKey('status.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    payment_method_id = db.Column(db.Integer, ForeignKey('payment_methods.id'), nullable=False)
    is_paid = db.Column(db.Boolean, nullable=False)
    phone_number = db.Column(db.Text, nullable=False)
    address_id = db.Column(db.Integer, ForeignKey('addresses.id'), nullable=False)
    admin_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)

    def __init__(self, id, date, user_id, status_id, payment_method_id, is_paid, phone_number, address_id):
        self.id = id
        self.date = date
        self.user_id = user_id
        self.status_id = status_id
        self.payment_method_id = payment_method_id
        self.is_paid = is_paid
        self.phone_number = phone_number
        self.address_id = address_id


class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, id, user_id, product_id, rating):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating


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
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, id, product_id, size, quantity):
        self.id = id
        self.product_id = product_id
        self.size = size
        self.quantity = quantity


class OrderedProduct(db.Model):
    __tablename__ = "ordered_products"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    product_price = db.Column(db.Numeric(10,2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, id, order_id, product_id, product_price, quantity):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.product_price = product_price
        self.quantity = quantity


class PaymentMethod(db.Model):
    __tablename__ = "payment_methods"

    id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.Text, nullable=False)

    def __init__(self, id, payment_method):
        self.id = id
        self.payment_method = payment_method


class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    brandname = db.Column(db.Text, nullable=False)

    def __init__(self, id, brandname):
        self.id = id
        self.brandname = brandname
