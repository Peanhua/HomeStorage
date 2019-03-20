from application import app, db
from application.homes.models import Home
from flask import redirect, render_template, request, url_for

# List of homes
@app.route("/homes", methods=["GET"])
def homes_index():
    return render_template("homes/list.html", homes = Home.query.all())


# Create new home
@app.route("/homes/new/")
def homes_form():
    return render_template("homes/new.html")

@app.route("/homes/", methods=["POST"])
def homes_create():
    home = Home(request.form.get("name"))

    db.session().add(home)
    db.session().commit()
    
    return redirect(url_for("homes_index"))
