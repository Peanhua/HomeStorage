from application                 import app, db
from application.storages.models import Storage
from application.storages.forms  import StorageForm
from flask                       import redirect, render_template, request, url_for

# List of storages
@app.route("/storages", methods=["GET"])
def storages_index():
    return render_template("storages/list.html", storages = Storage.query.all())


# Create new storage
@app.route("/storages/new/")
def storages_form():
    return render_template("storages/new.html", form = StorageForm())

@app.route("/storages/", methods=["POST"])
def storages_create():
    form = StorageForm(request.form)
    storage = Storage(form.name.data)

    db.session().add(storage)
    db.session().commit()
    
    return redirect(url_for("storages_index"))
