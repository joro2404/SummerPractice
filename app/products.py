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
