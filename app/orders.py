from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    #user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    status = db.Column(db.String(3), ForeignKey('status.statusCode'), nullable=False)

    def __init__(self, date, product_id, status):
        self.date = date
        #self.user_id = user_id
        self.product_id = product_id
        self.status = status

