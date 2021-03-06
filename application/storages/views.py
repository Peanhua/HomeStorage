from application                 import app, db, login_required, get_items_per_page
from application.storages.models import Storage
from application.storages.forms  import StorageForm, StorageEditForm, StorageDeleteForm
from application.homes.models    import Home
from application.items.models    import Item
from flask                       import redirect, render_template, request, url_for
from flask_login                 import current_user
from flask_wtf                   import FlaskForm

# List of storages
@app.route("/storages/", methods=["GET"], defaults={"page": 1})
@app.route("/storages/<int:page>", methods=["GET"])
@login_required()
def storages_index(page):
    homeids = [h.home_id for h in current_user.get_my_homes().all()]
    storages = db.session().query(Storage, Home.name).join(Home).filter(Home.home_id.in_(homeids)).order_by(Home.name, Storage.name).paginate(page=page, per_page=get_items_per_page(), error_out=False)
    if storages.page > 1 and storages.page > storages.pages:
        return redirect(url_for("storages_index"))
    return render_template("storages/list.html", storages=storages)


# Create new storage
@app.route("/storages/new/")
@login_required()
def storages_form():
    form = StorageForm()
    form.home.choices = [(h.home_id, h.name) for h in current_user.get_my_homes().all()]
    return render_template("storages/new.html", form = form)

@app.route("/storages/", methods=["POST"])
@login_required()
def storages_create():
    form = StorageForm(request.form)

    # Need to fill in the choices or the validator will crash:
    form.home.choices = [(h.home_id, h.name) for h in current_user.get_my_homes().all()]
    
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


# Storage edit:
@app.route("/storages/<storage_id>/edit", methods=["GET", "POST"])
@login_required()
def storages_edit(storage_id):
    storage = Storage.query.get(storage_id)
    if not storage:
        return redirect(url_for("auth_unauthorized"))
    home = Home.query.get(storage.home_id)

    if not home.is_user_in(current_user.user_id):
        return redirect(url_for("auth_unauthorized"))

    if request.method == "GET":
        form = StorageEditForm()
        form.name.data = storage.name
        return render_template("storages/edit.html", form=form, home=home, storage=storage)
    elif request.method == "POST":
        form = StorageEditForm(request.form)
        if not form.validate():
            return render_template("storages/edit.html", form=form, home=home, storage=storage)
        storage.name = form.name.data
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
        form = FlaskForm()
        return render_template("storages/stock_add.html", form=form, home=home, storage=storage, products=products)
            
    if request.method == "GET":
        return view()

    elif request.method == "POST":
        product_ids = request.form.getlist("productid[]")
        changes     = request.form.getlist("change[]")
        storage.adjust_stock(product_ids, changes)
        return redirect(url_for("storages_index"))

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
        form = FlaskForm()
        return render_template("storages/stock_remove.html", form=form, home=home, storage=storage, products=products)
            
    if request.method == "GET":
        return view()

    elif request.method == "POST":
        product_ids = request.form.getlist("productid[]")
        changes     = request.form.getlist("change[]")
        storage.adjust_stock(product_ids, changes)
        return redirect(url_for("storages_index"))

