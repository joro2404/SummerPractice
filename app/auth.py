from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .user import User
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('main.index'))

    else:
        if request.method == 'GET':
            return render_template('login.html')

        elif request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

            user = User.query.filter_by(email=email).first()
            
            if not user or not check_password_hash(user.password, password):
                flash('Please check your login credentials!')
                return redirect(url_for('auth.login'))

            login_user(user, remember=remember)

            return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are logged in!')
        return redirect(url_for('main.index'))

    else:
        if request.method == 'GET':
            return render_template('register.html')

        elif request.method == 'POST':
            email = request.form.get('email')
            name = request.form.get('name')
            password = request.form.get('password')
            confirm_password = request.form.get('password_confirm')

            user = User.query.filter_by(email=email).first()

            if user:
                flash('Email address already registered!')
                return redirect(url_for('auth.register'))

            if password != confirm_password:
                flash('Password missmatch!')
                return redirect(url_for('auth.register'))

            new_user = User(id=None, name=name, email=email, password=generate_password_hash(password, method='sha256'), admin=False, phone_number=None, address=None)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
