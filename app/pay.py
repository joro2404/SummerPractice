from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Product
from . import db



pay = Blueprint('pay', __name__)

@pay.route('/cart')
def cart():
    return render_template('cart.html')



@pay.route('/checkout')
def checkout():
    return render_template('checkout.html')


		
@pay.route('/add/<int:id>', methods=['POST'])
def add_product_to_cart(id):
	
	
    _quantity = int(request.form['quantity'])
    
    # validate the received values
    if _quantity and request.method == 'POST':
        row = Product.query.get(id)
        #print(row['id'])
        itemArray = { row.id : {'id' : row.id, 'name' : row.name, 'price' : float(row.price), 'quantity' : _quantity, 'total_price': _quantity * float(row.price)}}
        
        all_total_price = 0
        all_total_quantity = 0
        
        session.modified = True
        if 'cart_item' in session:
            if row['id'] in session['cart_item']:
                for key, value in session['cart_item'].items():
                    if row['id'] == key:

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
	try:
		session.clear()
		return redirect(url_for('products.view_catalog'))
	except Exception as e:
		print(e)

@pay.route('/delete/<string:id>')
def delete_product(id):
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		
		for item in session['cart_item'].items():
			if item[0] == id:				
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
		
		#return redirect('/')
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		
		