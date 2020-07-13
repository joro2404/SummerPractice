from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from sqlalchemy.sql import func
from sqlalchemy import or_
from .models import Product, Brand, Tag, ProductTags, Gender
import decimal


products = Blueprint('products', __name__)


@products.route('/catalog')
def redirect_to_catalog():
    return redirect(url_for('products.view_catalog', id=1))


@products.route('/catalog/<int:id>', methods=['GET', 'POST'])
def view_catalog(id):
    brands = Brand.query.all()
    tags = Tag.query.all()
    genders = Gender.query.all()
    products = Product.query.offset((id * 9) - 9).limit(id * 9).all()
    list_of_prices = [product.price for product in products]
    cheapest = min(list_of_prices)
    most_expensive = max(list_of_prices)


    if request.method == 'POST':
        brands_to_display = []
        genders_to_display = []
        tags_to_display = []

        min_price = request.form.get('minamount').strip('$')
        max_price = request.form.get('maxamount').strip('$')

        for brand in brands:
            brand_name = request.form.get(brand.brandname)

            if brand_name == 'on':
                print(brand.brandname)
                brands_to_display.append(brand)


        for gender in genders:
            gender_name = request.form.get(gender.gender)

            if gender_name == 'on':
                print(gender.gender)
                genders_to_display.append(gender)


        for tag in tags:
            tag_name = request.form.get(tag.tag)

            if tag_name == 'on':
                print(tag.tag)
                tags_to_display.append(tag)


        if brands_to_display:
            brands_names = [Brand.brandname == brand.brandname for brand in brands_to_display]

        else:
            brands_names = [Brand.brandname == brand.brandname for brand in brands]


        if genders_to_display:
            genders_ids = [Product.gender_id == gender.id for gender in genders_to_display]

        else:
            genders_ids = [Product.gender_id == gender.id for gender in genders]


        if tags_to_display:
            tags_ids = [ProductTags.tag_id == tag.id for tag in tags_to_display]

        else:
            tags_ids = [ProductTags.tag_id == tag.id for tag in tags]

        search_q = request.args.get('search')
        if search_q:
            search = "%{}%".format(search_q)
            products = db.session.query(Product) \
                .join(Brand, Brand.id == Product.brand_id) \
                .join(ProductTags, Product.id == ProductTags.product_id) \
                .join(Tag, ProductTags.tag_id == Tag.id) \
                .filter(or_(*brands_names)) \
                .filter(or_(*genders_ids)) \
                .filter(or_(*tags_ids)) \
                .filter(Product.price >= min_price, Product.price <= max_price) \
                .filter(Product.name.like(search)) \
                .all()

        else:
            products = db.session.query(Product) \
                .join(Brand, Brand.id == Product.brand_id) \
                .join(ProductTags, Product.id == ProductTags.product_id) \
                .join(Tag, ProductTags.tag_id == Tag.id) \
                .filter(or_(*brands_names)) \
                .filter(or_(*genders_ids)) \
                .filter(or_(*tags_ids)) \
                .filter(Product.price >= min_price, Product.price <= max_price) \
                .all()
    
        brands_products = []
        for product in products:
            brands_products.append(Brand.query.get(product.brand_id))

        return render_template('catalog.html', products=products, brands_products=brands_products, brands=brands, cheapest=cheapest, most_expensive=most_expensive, tags=tags, brands_to_display=brands_to_display, genders=genders, genders_to_display=genders_to_display, tags_to_display=tags_to_display, max_price=max_price, min_price=min_price)

    search_q = request.args.get('search')
    if search_q:
        search = "%{}%".format(search_q)
        products = Product.query.filter(Product.name.like(search)).all()

    brands_products = []
    for product in products:
        brands_products.append(Brand.query.get(product.brand_id))

    return render_template('catalog.html', products=products, brands_products=brands_products, brands=brands, cheapest=cheapest, most_expensive=most_expensive, tags=tags, genders=genders)


@products.route('/catalog/<int:id>')
def view_product(id):

    product = Product.query.get(id)
    discounted_price = decimal.Decimal(product.price) * decimal.Decimal(1.33)
    brand = Brand.query.get(product.brand_id)
    tags = db.session.query(ProductTags).filter(ProductTags.product_id == id)
    gender = Gender.query.get(product.gender_id)

    tag_names = []
    for tag in tags:
        var = Tag.query.get(tag.tag_id)
        tag_names.append(var.tag)
    
    tagstr = ""
    for i in range(0, len(tag_names)):
        tagstr += str(tag_names[i])
        if i != len(tag_names) - 1:
            tagstr += ", "

    
    return render_template('view_product.html', product=product, discounted_price=discounted_price, brand=brand, tags=tagstr, gender=gender.gender)
