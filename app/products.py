from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Product


products = Blueprint('products', __name__)


@products.route('/catalog')
def view_catalog():
    all_products = Product.query.all()
    print(all_products)
    return render_template('catalog.html')