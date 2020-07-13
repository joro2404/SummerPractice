from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from sqlalchemy.sql import func
from flask_login import login_user, logout_user, login_required, current_user
from .models import Product, Brand, Tag, ProductTags, Gender, User
import decimal


products = Blueprint('products', __name__)


@products.route('/catalog')
def view_catalog():
    cheapest = 0
    most_expensive = 0
    brands = Brand.query.all()
    tags = Tag.query.all()
    
    gender_form = request.args.get('gender')
    gender = None

    if (gender_form == 'Men'):
        gender = 1

    elif (gender_form == 'Women'):
        gender = 2

    elif (gender_form == 'Unisex'):
        gender = 3

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
        products = Product.query.filter_by(gender_id=gender).all()

        if (products):
            list_of_prices = [product.price for product in products]
            cheapest = min(list_of_prices)
            most_expensive = max(list_of_prices)

    else:
        products = db.session.query(Product) \
            .join(ProductTags, Product.id == ProductTags.product_id) \
            .join(Tag, ProductTags.tag_id == Tag.id) \
            .filter(Tag.tag == tag) \
            .filter(Product.gender_id == gender) \
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
    gender = Gender.query.get(product.gender_id)

    user = User.query.get(current_user.id) 

    tag_names = []
    for tag in tags:
        var = Tag.query.get(tag.tag_id)
        tag_names.append(var.tag)
    
    tagstr = ""
    for i in range(0, len(tag_names)):
        tagstr += str(tag_names[i])
        if i != len(tag_names) - 1:
            tagstr += ", "

    
    return render_template('view_product.html', user=user, product=product, discounted_price=discounted_price, brand=brand, tags=tagstr, gender=gender.gender)

@login_required
@products.route('/edit_product/<int:id>')
def edit_product(id):

    user = User.query.get(current_user.id)

    if user.is_admin:

        if request.method == 'POST':
            
            name = request.form.get('product_name')
            brand_id = request.form.get('brand')
            gender_id = request.form.get('gender')
            price = request.form.get('price')
            description = request.form.get('description')
            

            db.session.query(Order).filter_by(id=id).update({ 'name':name, 'price':float(price), 'brand_id':brand_id, 'gender_id': gender_id, 'description':description})
            db.session.commit()

            product = db.session.query(Product).filter_by(name=name).first()
            
            tags = db.session.query(ProductTags).filter_by(product_id=product.id).all()
            db.session.delete(tags)
            db.session.commit()

            i = 1
            while(request.form.get('tag_id_' + str(i)) is not None):
                tag_id = request.form.get('tag_id_' + str(i))
                new_tag = ProductTags(None, product.id, tag_id)
                db.session.add(new_tag)
                db.session.commit()
                i += 1
            return redirect(url_for('products.view_product', id=id))

        if request.method == 'GET':
            
            product = Product.query.get(id)
            brands = Brand.query.all()
            genders = Gender.query.all()
            tags = Tag.query.all()

            return render_template('edit_product.html', product=product, brands=brands, genders=genders, tags=tags)

    else:
        message = True
        return render_template('error.html', message=message)