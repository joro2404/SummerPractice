from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Raiting(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    raiting = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, product_id, raiting):
        #self.user_id = user_id
        self.product_id = product_id
        self.raiting = raiting