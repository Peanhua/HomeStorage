from application import app, db
from application.storages.models import Storage
from flask import redirect, render_template, request, url_for

# List of storages
@app.route("/storages", methods=["GET"])
def storages_index():
    return render_template("storages/list.html", storages = Storage.query.all())


# Create new storage
@app.route("/storages/new/")
def storages_form():
    return render_template("storages/new.html")

@app.route("/storages/", methods=["POST"])
def storages_create():
    storage = Storage(request.form.get("name"))

    db.session().add(storage)
    db.session().commit()
    
    return redirect(url_for("storages_index"))
