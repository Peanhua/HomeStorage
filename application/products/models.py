from application import db

class Product(db.Model):
    product_id       = db.Column(db.Integer,    primary_key = True)
    name             = db.Column(db.String(80), nullable = False)
    default_lifetime = db.Column(db.Integer,    nullable = False)

    def __init__(self, name, default_lifetime):
        self.name             = name
        self.default_lifetime = default_lifetime
        
