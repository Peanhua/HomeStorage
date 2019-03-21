from application import app, db
from application.users.models import User
from flask import redirect, render_template, request, url_for

# List of users
@app.route("/users", methods=["GET"])
def users_index():
    return render_template("users/list.html", users = User.query.all())


# Create new user
@app.route("/users/new/")
def users_form():
    return render_template("users/new.html")

@app.route("/users/", methods=["POST"])
def users_create():
    user = User(request.form.get("name"), request.form.get("email"), request.form.get("login"), request.form.get("password"))

    db.session().add(user)
    db.session().commit()
    
    return redirect(url_for("users_index"))
