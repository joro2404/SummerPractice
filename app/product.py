from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False)
    price = db.Column(db.Float(5, 2), unique=False)
    overallRaiting = db.Column(db.Float(1, 2), unique=False)
    #category = db.Column(db.Integer, ForeignKey('category.id'))

    def __init__(self, name, price, overallRaiting):
        self.name = name
        self.price = price
        self.overallRaiting = overallRaiting

