from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from sqlalchemy.sql import func
from .models import Product, Brand
import decimal


products = Blueprint('products', __name__)


@products.route('/catalog')
def view_catalog():
    products = Product.query.all()
    brands = Brand.query.all()
    cheapest = db.session.query(func.min(Product.price)).first()
    most_expensive = db.session.query(func.max(Product.price)).first()

    brands_products = []
    for product in products:
        brands_products.append(Brand.query.get(product.brand_id))

    return render_template('catalog.html', products=products, brands_products=brands_products, brands=brands, cheapest=cheapest[0], most_expensive=most_expensive[0])


@products.route('/product/<int:id>')
def view_product(id):

    product = Product.query.get(id)
    discounted_price = product.price * decimal.Decimal(1.33)
    brand = Brand.query.get(product.brand_id)
    return render_template('view_product.html', product=product, discounted_price=discounted_price, brand=brand)
