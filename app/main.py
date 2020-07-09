from flask import Flask, render_template, request, redirect, url_for, Blueprint
from .models import User
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    main.app.run()