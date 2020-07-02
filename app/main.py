from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from .product import Product
from .user import User
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', name=current_user.name)


if __name__ == '__main__':
    main.app.run()