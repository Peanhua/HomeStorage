from application                 import app, db, login_required
from application.storages.models import Storage
from application.storages.forms  import StorageForm, StorageDeleteForm
from application.homes.models    import Home
from application.items.models    import Item
from application.products.models import Product
from flask                       import redirect, render_template, request, url_for
from flask_login                 import current_user
from datetime                    import datetime, timedelta

# List of storages
@app.route("/storages", methods=["GET"])
@login_required()
def storages_index():
    homeids = [h.home_id for h in current_user.get_my_homes()]
    storages = db.session().query(Storage, Home.name).join(Home).filter(Home.home_id.in_(homeids)).order_by(Home.name, Storage.name).all()
    return render_template("storages/list.html", storages=storages)


# Create new storage
@app.route("/storages/new/")
@login_required()
def storages_form():
    form = StorageForm()
    form.home.choices = [(h.home_id, h.name) for h in current_user.get_my_homes()]
    return render_template("storages/new.html", form = form)

@app.route("/storages/", methods=["POST"])
@login_required()
def storages_create():
    form = StorageForm(request.form)

    # Need to fill in the choices or the validator will crash:
    form.home.choices = [(h.home_id, h.name) for h in current_user.get_my_homes()]
    
    if not form.validate():
        return render_template("storages/new.html", form = form)

    storage = Storage(form.home.data, form.name.data)

    db.session().add(storage)
    db.session().commit()
    
    return redirect(url_for("storages_index"))


# Storage delete:
@app.route("/storages/<storage_id>/delete", methods=["GET", "DELETE"])
@login_required()
def storages_delete(storage_id):
    # TODO: make sure the user has permission to delete this storage
    storage = Storage.query.get(storage_id)
    if request.method == "GET":
        home = Home.query.get(storage.home_id)
        stock = storage.get_stock(False)
        form = StorageDeleteForm(obj=storage)
        return render_template("storages/delete.html", form=form, home=home, storage=storage, stock=stock)
    elif request.method == "DELETE":
        db.session().delete(storage)
        db.session().commit()
        return url_for("storages_index")


# Stock edit
@app.route("/storages/<storage_id>/stock", methods=["GET", "POST"])
@login_required()
def stock_edit(storage_id):
    storage = Storage.query.get(storage_id)
    def view():
        home = Home.query.get(storage.home_id)
        products = storage.get_stock()
        homeproducts = home.get_stock_all()
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
