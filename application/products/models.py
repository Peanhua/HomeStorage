from application import db

class Product(db.Model):
    product_id = db.Column(db.Integer,    primary_key = True)
    name       = db.Column(db.String(80), nullable = False)

    def __init__(self, name):
        self.name = name
