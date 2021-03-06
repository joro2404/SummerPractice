from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Product, OrderedProduct, Order, Address, Status, Brand, Gender, Tag, ProductTags, Picture
from . import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os


admin = Blueprint('admin', __name__)
upload_folder = "/home/vesko/Desktop/online_store/SummerPractice/app/static/img/uploads"
default_img = "/home/vesko/Desktop/online_store/SummerPractice/app/static/img/products/women-1.jpg"


@login_required
@admin.route('/admin')
def view_admin():
    user = User.query.get(current_user.id)
    products = Product.query.all()

    from_date = request.args.get('from-date')
    to_date = request.args.get('to-date')
    order_way = request.args.get('order')

    order_by = ''

    if order_way:
        if order_way == 'desc':
            order_by = Order.date.desc()
        elif order_way == 'asc':
            order_by = Order.date.asc()

    else:
        order_by = Order.date.desc()
        

    if from_date and not to_date:
        orders = db.session.query(Order) \
            .filter(Order.date >= from_date) \
            .order_by(order_by) \
            .all()

    elif not from_date and to_date:
        orders = db.session.query(Order) \
            .filter(Order.date <= to_date) \
            .order_by(order_by) \
            .all()

    elif not from_date and not to_date:
        orders = Order.query.order_by(order_by).all()

    else:
        orders = db.session.query(Order) \
            .filter(Order.date >= from_date, Order.date <= to_date) \
            .order_by(order_by) \
            .all()

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
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                filename = secure_filename("/default.jpg")
                filepath = os.path.join("/static/img", filename)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                filepath = os.path.join("/static/img/uploads", filename)
            
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

            new_picture = Picture(None, product.id, filepath)
            db.session.add(new_picture)
            db.session.commit()
            
            return redirect(url_for('products.view_catalog', id=1))

        if request.method == 'GET':

            brands = Brand.query.all()
            genders = Gender.query.all()
            tags = Tag.query.all()

            return render_template('create_product.html', brands=brands, genders=genders, tags=tags)

    else:
        message = True
        return render_template('error.html', message=message)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS