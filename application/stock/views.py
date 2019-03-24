from application                 import app, db, login_required
from application.homes.models    import Home
from application.storages.models import Storage
from application.items.models    import Item
from flask                       import render_template, request, url_for
from flask_login                 import current_user


# Stock edit
@app.route("/stock/<home_id>/", methods=["GET", "POST"])
@login_required()
def stock_edit(home_id):
    home = Home.query.get(home_id)
    
    def view():
        storages = Storage.query.filter(Storage.home_id == home_id).all()
        products = home.get_stock()
        return render_template("homes/stock_edit.html", home=home, storages=storages, products=products)

    if request.method == "GET":
        return view()
    
    elif request.method == "POST":
        storage_id  = request.form["storage_id"]
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
