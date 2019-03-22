from application              import app, db
from application.users.models import User
from application.users.forms  import UserForm
from flask                    import redirect, render_template, request, url_for

# List of users
@app.route("/users", methods=["GET"])
def users_index():
    return render_template("users/list.html", users = User.query.all())


# Create new user
@app.route("/users/new/")
def users_form():
    return render_template("users/new.html", form = UserForm())

@app.route("/users/", methods=["POST"])
def users_create():
    form = UserForm(request.form)

    if not form.validate():
        return render_template("users/new.html", form = form)
    
    user = User(form.name.data,
                form.email.data,
                form.login.data,
                form.password.data)

    db.session().add(user)
    db.session().commit()
    
    return redirect(url_for("users_index"))
