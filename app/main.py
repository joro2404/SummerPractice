from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from .models import User
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


if __name__ == '__main__':
    main.app.run()