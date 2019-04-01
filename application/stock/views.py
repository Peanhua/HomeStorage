from application                 import app, db, login_required
from application.homes.models    import Home
from application.storages.models import Storage
from application.items.models    import Item
from application.products.models import Product
from flask                       import render_template, request, url_for
from flask_login                 import current_user
from datetime                    import datetime, timedelta


# Stock edit
@app.route("/stock/<storage_id>/", methods=["GET", "POST"])
@login_required()
def stock_edit(storage_id):
    storage = Storage.query.get(storage_id)
    def view():
        home = Home.query.get(storage.home_id)
        products = storage.get_stock()
        homeproducts = home.get_stock()
        for product in products:
            hp = next(p for p in homeproducts if p["product_id"] == product["product_id"])
            product["current_total_quantity"] = hp["current_quantity"]
        return render_template("storages/stock_edit.html", home=home, storage=storage, products=products)

    if request.method == "GET":
        return view()
    
    elif request.method == "POST":
        product_ids = request.form.getlist("productid[]")
        changes     = request.form.getlist("change[]")

        for product_id in product_ids:
            ind = product_ids.index(product_id)
            amount = int(changes[ind])
            if amount < 0: # Remove or adjust quantities for negative changes:
                amount = -amount
                while amount > 0:
                    amount = storage.decrease_item_count(product_id, amount)
            elif amount > 0: # Add new items:
                product = Product.query.get(product_id)
                bestbefore = datetime.now() + timedelta(days=product.default_lifetime)
                item = Item(product_id, storage_id, bestbefore)
                item.quantity = amount
                db.session().add(item)

        db.session().commit()

        return view()
