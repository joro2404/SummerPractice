from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Favourite(db.Model):
    __tablename__ = "favourites"
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)

    def __init__(self, product_id):
        #self.user_id = user_id
        self.product_id = product_id