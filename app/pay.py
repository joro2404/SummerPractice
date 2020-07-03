from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db



pay = Blueprint('pay', __name__)

@pay.route('/cart')
def cart():
    return render_template('cart.html')



@pay.route('/checkout')
def checkout():
    return render_template('checkout.html')
