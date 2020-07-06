from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Product, Brand
import decimal


products = Blueprint('products', __name__)


@products.route('/catalog')
def view_catalog():
    all_products = Product.query.all()
    print(all_products)
    return render_template('catalog.html')


@products.route('/product/<int:id>')
def view_product(id):

    product = Product.query.get(id)
    discounted_price = product.price * decimal.Decimal(1.33)
    brand = Brand.query.get(product.brand_id)
    return render_template('view_product.html', product=product, discounted_price=discounted_price, brand=brand)