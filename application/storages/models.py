from application              import db
from application.items.models import Item
from sqlalchemy.sql           import text

class Storage(db.Model):
    storage_id = db.Column(db.Integer,    primary_key = True)
    home_id    = db.Column(db.Integer,    db.ForeignKey("home.home_id"), nullable = False)
    name       = db.Column(db.String(80),                                nullable = False)

    def __init__(self, home_id, name):
        self.home_id = home_id
        self.name    = name

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
                 "                          AND item.storage_id = :storage_id"
                 " GROUP BY product.product_id"
                ).params(home_id=self.home_id,
                         storage_id=self.storage_id)
        res = db.engine.execute(q)
        rv = []
        for row in res:
            rv.append({"product_id":           row[0],
                       "product_name":         row[1],
                       "desired_min_quantity": row[2] if row[2] else 0,
                       "desired_max_quantity": row[3] if row[3] else 0,
                       "current_quantity":     row[4] if row[4] else 0
                       })
        return rv

    def decrease_item_count(self, product_id, amount):
        # Removes the amount number of items if found for the given product_id,
        # returns the amount that was not removed.
        item = Item.query.filter(Item.storage_id == self.storage_id, Item.product_id == product_id).order_by(Item.best_before).first()
        if not item:
            return amount

        if item.quantity <= amount:
            amount -= item.quantity
            db.session().delete(item)
            return amount
        else:
            item.quantity -= amount
            db.session().commit()
            return 0
