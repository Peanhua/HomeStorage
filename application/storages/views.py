from application                 import app, db, login_required
from application.storages.models import Storage
from application.storages.forms  import StorageForm, StorageDeleteForm
from application.homes.models    import Home
from application.items.models    import Item
from flask                       import redirect, render_template, request, url_for
from flask_login                 import current_user

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

    home = Home.query.get(form.home.data)
    if not home:
        return redirect(url_for("auth_unauthorized"))
    if not home.is_user_in(current_user.user_id):
        return redirect(url_for("auth_unauthorized"))
    
    storage = Storage(home.home_id, form.name.data)

    db.session().add(storage)
    db.session().commit()
    
    return redirect(url_for("storages_index"))


# Storage delete:
@app.route("/storages/<storage_id>/delete", methods=["GET", "DELETE"])
@login_required()
def storages_delete(storage_id):
    storage = Storage.query.get(storage_id)
    if not storage:
        return redirect(url_for("auth_unauthorized"))
    home = Home.query.get(storage.home_id)

    if not home.is_user_in(current_user.user_id):
        return redirect(url_for("auth_unauthorized"))

    if request.method == "GET":
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
    if not storage:
        return redirect(url_for("auth_unauthorized"))
    home = Home.query.get(storage.home_id)

    if not home.is_user_in(current_user.user_id):
        return redirect(url_for("auth_unauthorized"))
    
    def view():
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
        storage.adjust_stock(product_ids, changes)
        return view()


@app.route("/storages/<storage_id>/add_items", methods=["GET", "POST"])
@login_required()
def stock_add(storage_id):
    storage = Storage.query.get(storage_id)
    if not storage:
        return redirect(url_for("auth_unauthorized"))
    home = Home.query.get(storage.home_id)

    if not home.is_user_in(current_user.user_id):
        return redirect(url_for("auth_unauthorized"))
    
    def view():
        products = storage.get_stock()
        return render_template("storages/stock_add.html", home=home, storage=storage, products=products)
            
    if request.method == "GET":
        return view()

    elif request.method == "POST":
        product_ids = request.form.getlist("productid[]")
        changes     = request.form.getlist("change[]")
        storage.adjust_stock(product_ids, changes)
        return view()

@app.route("/storages/<storage_id>/remove_items", methods=["GET", "POST"])
@login_required()
def stock_remove(storage_id):
    storage = Storage.query.get(storage_id)
    if not storage:
        return redirect(url_for("auth_unauthorized"))
    home = Home.query.get(storage.home_id)

    if not home.is_user_in(current_user.user_id):
        return redirect(url_for("auth_unauthorized"))
    
    def view():
        products = storage.get_stock()
        return render_template("storages/stock_remove.html", home=home, storage=storage, products=products)
            
    if request.method == "GET":
        return view()

    elif request.method == "POST":
        product_ids = request.form.getlist("productid[]")
        changes     = request.form.getlist("change[]")
        storage.adjust_stock(product_ids, changes)
        return view()

