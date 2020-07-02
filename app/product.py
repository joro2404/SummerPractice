from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False, nullable=False)
    price = db.Column(db.Float(5, 2), unique=False, nullable=False)
    overallRaiting = db.Column(db.Float(1, 2), unique=False, nullable=False)
    #category = db.Column(db.Integer, ForeignKey('category.id'), nullable=False)

    def __init__(self, name, price, overallRaiting):
        self.name = name
        self.price = price
        self.overallRaiting = overallRaiting
        #self.category = category

