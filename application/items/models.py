from application                 import db
from sqlalchemy.sql              import text

class Item(db.Model):
    item_id    = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable = False)
    storage_id = db.Column(db.Integer, db.ForeignKey("storage.storage_id", ondelete="CASCADE"), nullable = False)
    quantity   = db.Column(db.Integer, nullable = False)
    best_before = db.Column(db.Date,   nullable = False)

    #storage = db.relationship("Storage", backref=backref("Item", passive_deletes=True))

    def __init__(self, product_id, storage_id, best_before):
        self.product_id  = product_id
        self.storage_id  = storage_id
        self.quantity    = 0
        self.best_before = best_before

    @staticmethod
    def get_total():
        q = text("SELECT SUM(quantity) FROM item")
        res = db.engine.execute(q)
        count = res.fetchone()[0]
        if count == None:
            count = 0
        res.close()
        return count
    
