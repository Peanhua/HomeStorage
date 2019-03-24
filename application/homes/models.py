from application import db

class Home(db.Model):
    home_id  = db.Column(db.Integer,    primary_key = True)
    name     = db.Column(db.String(80), nullable = False)

    users = db.relationship("HomeUser", backref="home", lazy=True)
    #users = db.relationship("HomeUser", back_populates="users")

    def __init__(self, name):
        self.name     = name


class HomeUser(db.Model):
    homeuser_id = db.Column(db.Integer, primary_key = True)
    home_id     = db.Column(db.Integer, db.ForeignKey("home.home_id"),    nullable = False)
    user_id     = db.Column(db.Integer, db.ForeignKey("account.user_id"), nullable = False)

    #home = db.relationship("Home")
    user = db.relationship("User")

    def __init__(self, home_id, user_id):
        self.home_id = home_id
        self.user_id = user_id


class HomeProduct(db.Model):
    homeproduct_id       = db.Column(db.Integer, primary_key = True)
    home_id              = db.Column(db.Integer, db.ForeignKey("home.home_id"),       nullable = False)
    product_id           = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable = False)
    desired_min_quantity = db.Column(db.Integer, nullable = True)
    desired_max_quantity = db.Column(db.Integer, nullable = True)

    def __init__(self, home_id, product_id, desired_min_quantity, desired_max_quantity):
        self.home_id              = home_id
        self.product_id           = product_id
        self.desired_min_quantity = desired_min_quantity
        self.desired_max_quantity = desired_max_quantity
