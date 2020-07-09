from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Address, Order, OrderedProduct, Product, Status
from . import db


profile = Blueprint('profile', __name__)


@profile.route('/profile')
@login_required
def view_profile():
    address = db.session.query(Address).filter_by(user_id=current_user.id).first()

    orders = db.session.query(Order).filter_by(user_id=current_user.id).limit(5).all()

    products = Product.query.all()

    statuses = Status.query.all()

    total_price = 0
    orders_total_price = []
    orders_products = []

    for order in orders:
        order_products = db.session.query(OrderedProduct).filter_by(order_id=order.id).all()
        orders_products.append(order_products)

        for order_product in order_products:
            total_price += order_product.product_price * order_product.quantity

        orders_total_price.append(total_price)
        total_price = 0

    return render_template('profile.html', address = address, orders=orders, orders_products=orders_products, orders_total_price=orders_total_price, products=products, statuses=statuses)


@profile.route('/profile/my_orders')
@login_required
def view_orders():
    orders = db.session.query(Order).filter_by(user_id=current_user.id).all()

    products = Product.query.all()

    statuses = Status.query.all()

    total_price = 0
    orders_total_price = []
    orders_products = []

    for order in orders:
        order_products = db.session.query(OrderedProduct).filter_by(order_id=order.id).all()
        orders_products.append(order_products)

        for order_product in order_products:
            total_price += order_product.product_price * order_product.quantity

        orders_total_price.append(total_price)
        total_price = 0

    return render_template('my_orders.html', orders=orders, orders_products=orders_products, orders_total_price=orders_total_price, products=products, statuses=statuses)


@profile.route('/profile/orders/<int:id>')
@login_required
def view_order(id):
    order = db.session.query(Order).filter_by(id=id).first()

    address = db.session.query(Address).filter_by(id=order.address_id).first()

    products = Product.query.all()

    statuses = Status.query.all()

    total_price = 0

    order_products = db.session.query(OrderedProduct).filter_by(order_id=order.id).all()

    for order_product in order_products:
        total_price += order_product.product_price * order_product.quantity

    print(order)
    print(address)

    return render_template('view_order.html', order=order, order_products=order_products, products=products, statuses=statuses, address=address, total_price=total_price)


@profile.route('/profile/my_addresses')
@login_required
def view_addresses():
    addresses = db.session.query(Address).filter_by(user_id=current_user.id).all()

    return render_template('my_addresses.html', addresses=addresses)


@profile.route('/profile/my_addresses/new', methods=['GET', 'POST'])
@login_required
def new_address():
    if request.method == 'POST':
        name = request.form.get('receiver-name')
        phone = request.form.get('receiver-phone')
        address = request.form.get('address')

        new_address = Address(None, current_user.id, name, phone, address)

        db.session.add(new_address)
        db.session.commit()
        
        flash('Success', 'success')
        return redirect(url_for('profile.view_addresses'))

    return render_template('new_address.html')


@profile.route('/profile/my_addresses/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_address(id):
    address = db.session.query(Address).filter_by(id=id).first()

    if request.method == 'POST':
        name = request.form.get('receiver-name')
        phone = request.form.get('receiver-phone')
        address = request.form.get('address')

        db.session.query(Address).filter_by(id=id).update({ 'receiver_name':name, 'receiver_phone': phone, 'address': address })
        db.session.commit()
        
        flash('Success', 'success')
        return redirect(url_for('profile.view_addresses'))


    if not address.user_id == current_user.id:
        flash('MANQK KUDE BARASH', 'danger')
        return redirect(url_for('profile.view_profile'))

    else:
        return render_template('edit_address.html', address=address)


    return render_template('edit_address.html', address=address)


@profile.route('/profile/my_addresses/<int:id>/delete', methods=['POST'])
@login_required
def delete_address(id):
    address = db.session.query(Address).filter_by(id=id).first()

    if address.user_id == current_user.id:
        db.session.delete(address)
        db.session.commit()

        flash('Successfuly deleted the address!', 'success')
        return redirect(url_for('profile.view_addresses'))

    flash('MANQK KUDE BARASH', 'danger')
    return redirect(url_for('profile.view_addresses'))


@profile.route('/profile/settings', methods=['GET', 'POST'])
@login_required
def view_settings():

    return render_template('settings.html')


@profile.route('/profile/settings/change_name', methods=['POST'])
@login_required
def change_name():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    phone = request.form.get('phone')

    db.session.query(User).filter_by(email=current_user.email).update({ 'phone_number':phone, 'first_name': first_name, 'last_name': last_name })
    db.session.commit()

    return redirect(url_for('profile.view_settings'))


@profile.route('/profile/settings/change_password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('old-password')
    new_password = request.form.get('new-password')
    confirm_new_password = request.form.get('new-password-confirm')

    if check_password_hash(current_user.password, old_password) and new_password == confirm_new_password:
        new_password_hash = generate_password_hash(new_password, method='sha256')

        db.session.query(User).filter_by(email=current_user.email).update({ 'password':new_password_hash })
        db.session.commit()
        flash('Success', 'success')
        return redirect(url_for('profile.view_settings'))
    
    elif not check_password_hash(current_user.password, old_password):
        flash('Old password is wrong!', 'danger')
        return redirect(url_for('profile.view_settings'))

    elif new_password != confirm_new_password:
        flash('Passwords don\'t match!', 'danger')
        return redirect(url_for('profile.view_settings'))

    return redirect(url_for('profile.view_settings'))