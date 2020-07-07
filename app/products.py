from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from sqlalchemy.sql import func
from .models import Product, Brand, Tag, ProductTags
import decimal


products = Blueprint('products', __name__)


@products.route('/catalog')
def view_catalog():
    cheapest = 0
    most_expensive = 0
    brands = Brand.query.all()
    tags = Tag.query.all()
    
    gender = request.args.get('gender')
    tag = request.args.get('tags')

    if (tag == None and gender == None):
        products = Product.query.all()

        list_of_prices = [product.price for product in products]
        cheapest = min(list_of_prices)
        most_expensive = max(list_of_prices)

    elif (tag != None and gender == None):
        products = db.session.query(Product) \
            .join(ProductTags, Product.id == ProductTags.product_id) \
            .join(Tag, ProductTags.tag_id == Tag.id) \
            .filter(Tag.tag == tag) \
            .all()

        list_of_prices = [product.price for product in products]
        cheapest = min(list_of_prices)
        most_expensive = max(list_of_prices)


    elif (tag == None and gender != None):    
        products = Product.query.filter_by(gender=gender).all()

        if (products):
            list_of_prices = [product.price for product in products]
            cheapest = min(list_of_prices)
            most_expensive = max(list_of_prices)

    else:
        products = db.session.query(Product) \
            .join(ProductTags, Product.id == ProductTags.product_id) \
            .join(Tag, ProductTags.tag_id == Tag.id) \
            .filter(Tag.tag == tag) \
            .filter(Product.gender == gender) \
            .all()
        
        if (products):
            list_of_prices = [product.price for product in products]
            cheapest = min(list_of_prices)
            most_expensive = max(list_of_prices)

    brands_products = []
    for product in products:
        brands_products.append(Brand.query.get(product.brand_id))

    return render_template('catalog.html', products=products, brands_products=brands_products, brands=brands, cheapest=cheapest, most_expensive=most_expensive, tags=tags)


@products.route('/catalog/<int:id>')
def view_product(id):

    product = Product.query.get(id)
    discounted_price = product.price * decimal.Decimal(1.33)
    brand = Brand.query.get(product.brand_id)
    return render_template('view_product.html', product=product, discounted_price=discounted_price, brand=brand)
