from application                 import app, db
from application.storages.models import Storage
from application.storages.forms  import StorageForm
from application.homes.models    import Home
from flask                       import redirect, render_template, request, url_for
from flask_login                 import current_user, login_required

# Helper function:
def get_my_homes():
    Home.query.order_by("name")
    
# List of storages
@app.route("/storages", methods=["GET"])
@login_required
def storages_index():
    return render_template("storages/list.html", storages = Storage.query.all())


# Create new storage
@app.route("/storages/new/")
@login_required
def storages_form():
    form = StorageForm()
    form.home.choices = [(h.home_id, h.name) for h in get_my_homes()]
    return render_template("storages/new.html", form = form)

@app.route("/storages/", methods=["POST"])
@login_required
def storages_create():
    form = StorageForm(request.form)

    # Need to fill in the choices or the validator will crash:
    form.home.choices = [(h.home_id, h.name) for h in get_my_homes()]
    
    if not form.validate():
        return render_template("storages/new.html", form = form)

    storage = Storage(form.home.data, form.name.data)

    db.session().add(storage)
    db.session().commit()
    
    return redirect(url_for("storages_index"))
