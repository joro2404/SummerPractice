from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Product, OrderedProduct, Order, Address, Status
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
@admin.route('/queue')
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