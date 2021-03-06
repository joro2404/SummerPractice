from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Product, OrderedProduct, Order, Address
from . import db
from datetime import datetime



pay = Blueprint('pay', __name__)

@pay.route('/cart')
def cart():
    #session.clear()
    #session["test"] = "vesko"
    print(session.get("cart_item"))

    total_price = session.get('all_total_price')
    cart_items = session.get('cart_item')
    product_list = []

    if cart_items:
        cart_ids = list(cart_items.keys())

        for i in range(len(cart_ids)):
            cart_ids[i] = int(cart_ids[i])

        #print(cart_ids)

        for id in cart_ids:
            product = Product.query.get(id)
            product.quantity = cart_items[str(id)]['quantity']
            product_list.append(product)
        
        #print(product.quantity)

        return render_template('cart.html', products=product_list, total_price=total_price)

    else : 
        return render_template('cart.html', products=product_list, total_price=0)


@login_required
@pay.route('/checkout')
def checkout():

    total_price = session.get('all_total_price')
    cart_items = session.get('cart_item')
    addresses = db.session.query(Address).filter_by(user_id=current_user.id).all()
    product_list = []

    if cart_items:
        cart_ids = list(cart_items.keys())

        for i in range(len(cart_ids)):
            cart_ids[i] = int(cart_ids[i])

        for id in cart_ids:
            product = Product.query.get(id)
            product.quantity = cart_items[str(id)]['quantity']
            product_list.append(product)
        

        return render_template('checkout.html', products=product_list, total_price=total_price, addresses=addresses)


    else : 
        return render_template('checkout.html', products=product_list, total_price=0, addresses=addresses)


@login_required
@pay.route('/checkout/order', methods=['POST'])
def new_order():

    total_price = session.get('all_total_price')
    cart_items = session.get('cart_item')
    product_list = []

    address = request.form.get('address')

    if cart_items:
        cart_ids = list(cart_items.keys())

        order = Order(None, datetime.today().strftime('%Y-%m-%d'), current_user.id, 1, 1, False, address)
        db.session.add(order)
        db.session.commit()

        for i in range(len(cart_ids)):
            cart_ids[i] = int(cart_ids[i])

        for id in cart_ids:
            product = Product.query.get(id)
            product.quantity = cart_items[str(id)]['quantity']
            product_list.append(product)

        for product in product_list:
            ordered_product = OrderedProduct(None, order.id, product.id, product.price, product.quantity)
            db.session.add(ordered_product)
            db.session.commit()

        return redirect(url_for('pay.empty_cart'))

    else : 
        return redirect(url_for('pay.checkout'))


@login_required
@pay.route('/checkout/paypal', methods=['POST'])
def paypal():

    total_price = session.get('all_total_price')
    cart_items = session.get('cart_item')
    product_list = []

    address = request.form.get('address')

    if cart_items:
        cart_ids = list(cart_items.keys())

        order = Order(None, datetime.today().strftime('%Y-%m-%d'), current_user.id, 1, 1, True, address)
        db.session.add(order)
        db.session.commit()

        for i in range(len(cart_ids)):
            cart_ids[i] = int(cart_ids[i])

        for id in cart_ids:
            product = Product.query.get(id)
            product.quantity = cart_items[str(id)]['quantity']
            product_list.append(product)

        for product in product_list:
            ordered_product = OrderedProduct(None, order.id, product.id, product.price, product.quantity)
            db.session.add(ordered_product)
            db.session.commit()

        return redirect(url_for('pay.empty_cart'))

    else : 
        return redirect(url_for('pay.checkout'))


		
@pay.route('/add/<int:id>', methods=['POST'])
def add_product_to_cart(id):
	
	
    _quantity = int(request.form['quantity'])
    
    # validate the received values
    if _quantity and request.method == 'POST':
        row = Product.query.get(id)
        
        row.price = float(row.price)
        print(type(row.price))

        total_price = _quantity * row.price
        itemArray = { str(row.id) : {'id' : row.id, 'name' : row.name, 'price' : float(row.price), 'quantity' : _quantity, 'total_price': float(total_price)}}
        
        all_total_price = 0
        all_total_quantity = 0
        
        session.modified = True
        if 'cart_item' in session:
            
            if row.id in session['cart_item']:
                for key, value in session['cart_item'].items():
                    if row.id == key: 

                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + _quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = total_quantity * row.price
            else:
                session['cart_item'] = array_merge(session['cart_item'], itemArray)

            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price
        else:
            session['cart_item'] = itemArray
            all_total_quantity = all_total_quantity + _quantity
            all_total_price = all_total_price + _quantity * row.price
            
        
        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price
        
        return redirect(url_for('products.view_product',id=row.id))
    
	

		
@pay.route('/empty')
def empty_cart():
	
    session['cart_item'].clear()
    session['all_total_quantity'] = 0
    session['all_total_price'] = 0
    return redirect(url_for('profile.view_profile'))



	
@pay.route('/delete/<int:id>')
def delete_product(id):

    all_total_price = 0
    all_total_quantity = 0
    session.modified = True
    
    for item in session['cart_item'].items():
        if item[0] == str(id):				
            session['cart_item'].pop(item[0], None)
            if 'cart_item' in session:
                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            break
    
    if all_total_quantity == 0:
        session.clear()
    else:
        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price
    
    return redirect(url_for('pay.cart'))
	
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		
		