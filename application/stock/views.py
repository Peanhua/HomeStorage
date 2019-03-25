from application                 import app, db, login_required
from application.homes.models    import Home
from application.storages.models import Storage
from application.items.models    import Item
from flask                       import render_template, request, url_for
from flask_login                 import current_user


# Stock edit
@app.route("/stock/<storage_id>/", methods=["GET", "POST"])
@login_required()
def stock_edit(storage_id):
    def view():
        storage = Storage.query.get(storage_id)
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

        existing_items = Item.query.filter(Item.storage_id == storage_id).all()

        handled = []
        for ei in existing_items:
            try:
                ind = product_ids.index(ei.product_id)
                handled.append(ei.product_id)
                ei.quantity += changes[ind]
                if ei.quantity == 0:
                    db.session().delete(ei)
            except ValueError:
                pass
        
        for i in range(len(changes)):
            if product_ids[i] not in handled:
                item = Item(product_ids[i], storage_id)
                item.quantity = changes[i]
                db.session().add(item)

        db.session().commit()

        return view()
