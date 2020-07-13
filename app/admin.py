from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Product, OrderedProduct, Order, Address, Status, Brand, Gender, Tag, ProductTags
from . import db
from datetime import datetime



admin = Blueprint('admin', __name__)


@login_required
@admin.route('/admin')
def view_admin():

    user = User.query.get(current_user.id)

    products = Product.query.all()
    orders = Order.query.all()
    statuses = Status.query.all()
    total_price = 0
    orders_total_price = []
    orders_products = []


    if user.is_admin:

        for order in orders:
            order_products = db.session.query(OrderedProduct).filter_by(order_id=order.id).all()
            orders_products.append(order_products)

            for order_product in order_products:
                total_price += order_product.product_price * order_product.quantity

            orders_total_price.append(total_price)
            total_price = 0

        return render_template('view_admin.html', orders=orders, orders_products=orders_products, orders_total_price=orders_total_price, products=products, statuses=statuses)

    else:
        message = True
        return render_template('error.html', message=message)


@login_required
@admin.route('/admin/queue')
def queue():

    user = User.query.get(current_user.id)

    products = Product.query.all()
    orders = db.session.query(Order).filter_by(status_id=1).all()
    statuses = Status.query.all()
    total_price = 0
    orders_total_price = []
    orders_products = []


    if user.is_admin:

        for order in orders:
            order_products = db.session.query(OrderedProduct).filter_by(order_id=order.id).all()
            orders_products.append(order_products)

            for order_product in order_products:
                total_price += order_product.product_price * order_product.quantity

            orders_total_price.append(total_price)
            total_price = 0

        return render_template('queue.html', orders=orders, orders_products=orders_products, orders_total_price=orders_total_price, products=products, statuses=statuses)

    else:
        message = True
        return render_template('error.html', message=message)


@login_required
@admin.route('/admin/take_order/<int:id>')
def take_order(id):

    user = User.query.get(current_user.id)

    if user.is_admin:

        db.session.query(Order).filter_by(id=id).update({ 'status_id':2, 'admin_id': user.id})
        db.session.commit()

        
        return redirect(url_for('admin.queue'))

    else:
        message = True
        return render_template('error.html', message=message)


@login_required
@admin.route('/admin/accepted')
def accepted():

    user = User.query.get(current_user.id)

    products = Product.query.all()
    orders = db.session.query(Order).filter_by(status_id=2).all()
    statuses = Status.query.all()
    total_price = 0
    orders_total_price = []
    orders_products = []

    if user.is_admin:

        
        for order in orders:
            order_products = db.session.query(OrderedProduct).filter_by(order_id=order.id).all()
            orders_products.append(order_products)

            for order_product in order_products:
                total_price += order_product.product_price * order_product.quantity

            orders_total_price.append(total_price)
            total_price = 0

        return render_template('accepted.html', orders=orders, orders_products=orders_products, orders_total_price=orders_total_price, products=products, statuses=statuses)
        

    else:
        message = True
        return render_template('error.html', message=message)


@login_required
@admin.route('/admin/finish_order/<int:id>')
def finish_order(id):

    user = User.query.get(current_user.id)

    if user.is_admin:

        db.session.query(Order).filter_by(id=id).update({ 'status_id':4})
        db.session.commit()

        
        return redirect(url_for('admin.accepted'))

    else:
        message = True
        return render_template('error.html', message=message)



@login_required
@admin.route('/admin/create_product', methods=['GET', 'POST'])
def create_product():

    user = User.query.get(current_user.id)

    if user.is_admin:

        if request.method == 'POST':
            
            name = request.form.get('product_name')
            brand_id = request.form.get('brand')
            gender_id = request.form.get('gender')
            price = request.form.get('price')
            description = request.form.get('description')

            new_product = Product(None, name, float(price), brand_id, 0, gender_id, description)

            db.session.add(new_product)
            db.session.commit()

            product = db.session.query(Product).filter_by(name=name).first()
            i = 1
            while(request.form.get('tag_id_' + str(i)) is not None):
                tag_id = request.form.get('tag_id_' + str(i))
                new_tag = ProductTags(None, product.id, tag_id)
                db.session.add(new_tag)
                db.session.commit()
                i += 1
            return redirect(url_for('products.view_catalog'))

        if request.method == 'GET':

            brands = Brand.query.all()
            genders = Gender.query.all()
            tags = Tag.query.all()

            return render_template('create_product.html', brands=brands, genders=genders, tags=tags)

    else:
        message = True
        return render_template('error.html', message=message)