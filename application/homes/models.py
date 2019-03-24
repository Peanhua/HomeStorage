from application    import db
from sqlalchemy.sql import text

class Home(db.Model):
    home_id  = db.Column(db.Integer,    primary_key = True)
    name     = db.Column(db.String(80), nullable = False)

    users = db.relationship("HomeUser", backref="home", lazy=True)
    #users = db.relationship("HomeUser", back_populates="users")

    def __init__(self, name):
        self.name     = name

    def get_stock(self):
        q = text("SELECT product.product_id                AS product_id,"
                 "       product.name                      AS product_name,"
                 "       home_product.desired_min_quantity AS desired_min_quantity,"
                 "       home_product.desired_max_quantity AS desired_max_quantity,"
                 "       SUM(item.quantity)                AS current_quantity"
                 "  FROM product"
                 "       LEFT OUTER JOIN home_product ON product.product_id = home_product.product_id"
                 "                                       AND ( home_product.home_id = :home_id OR home_product.home_id IS NULL)"
                 "  LEFT OUTER JOIN item ON product.product_id = item.product_id"
                 "                          AND item.storage_id IN ( SELECT storage.storage_id"
                 "                                                     FROM storage"
                 "                                                    WHERE storage.home_id = :home_id )"
                 " GROUP BY product.product_id"
                ).params(home_id=self.home_id)
        res = db.engine.execute(q)
        rv = []
        for row in res:
            rv.append({"product_id":           row[0],
                       "product_name":         row[1],
                       "desired_min_quantity": row[2],
                       "desired_max_quantity": row[3],
                       "current_quantity":     row[4] if row[4] else 0
                       })
        return rv


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
