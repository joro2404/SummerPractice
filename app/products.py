from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from sqlalchemy.sql import func
from .models import Product, Brand, ProductTags, Tag
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


@products.route('/catalog/<int:id>')
def view_product(id):

    product = Product.query.get(id)
    discounted_price = decimal.Decimal(product.price) * decimal.Decimal(1.33)
    brand = Brand.query.get(product.brand_id)
    tags = db.session.query(ProductTags).filter(ProductTags.product_id == id)

    tag_names = []
    for tag in tags:
        var = Tag.query.get(tag.tag_id)
        tag_names.append(var.tag)
    
    tagstr = ""
    for i in range(0, len(tag_names)):
        tagstr += str(tag_names[i])
        if i != len(tag_names) - 1:
            tagstr += ", "

    
    return render_template('view_product.html', product=product, discounted_price=discounted_price, brand=brand, tags=tagstr)
