from application                 import app, db
from application.storages.models import Storage
from application.storages.forms  import StorageForm
from flask                       import redirect, render_template, request, url_for
from flask_login                 import login_required

# List of storages
@app.route("/storages", methods=["GET"])
@login_required
def storages_index():
    return render_template("storages/list.html", storages = Storage.query.all())


# Create new storage
@app.route("/storages/new/")
@login_required
def storages_form():
    return render_template("storages/new.html", form = StorageForm())

@app.route("/storages/", methods=["POST"])
@login_required
def storages_create():
    form = StorageForm(request.form)

    if not form.validate():
        return render_template("storages/new.html", form = form)
    
    storage = Storage(form.name.data)

    db.session().add(storage)
    db.session().commit()
    
    return redirect(url_for("storages_index"))
