from application                 import db
#from application.storages.models import Storage # This does not work because of recursive imports

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
