from application              import app, db
from application.users.models import User
from application.users.forms  import UserNewForm, UserEditForm
from flask                    import redirect, render_template, request, url_for
from flask_login              import current_user, login_required

# List of users
@app.route("/users", methods=["GET"])
@login_required
def users_index():
    return render_template("users/list.html", users = User.query.all())


# Create new user
@app.route("/users/new/")
@login_required
def users_form():
    return render_template("users/new.html", form = UserNewForm())

@app.route("/users/", methods=["POST"])
@login_required
def users_create():
    form = UserNewForm(request.form)

    if not form.validate():
        return render_template("users/new.html", form = form)
    
    user = User(form.name.data,
                form.email.data,
                form.login.data,
                form.password.data)

    user.superuser = form.superuser.data
    
    db.session().add(user)
    db.session().commit()
    
    return redirect(url_for("users_index"))


# Edit user
@app.route("/users/<user_id>/", methods=["GET", "POST", "DELETE"])
@login_required
def users_edit(user_id):
    user = User.query.get(user_id)

    if request.method == "GET":
        form = UserEditForm(obj=user)
        return render_template("users/edit.html", form=form, user=user)

    elif request.method == "POST":
        form = UserEditForm(request.form)

        if not form.validate():
            return render_template("users/edit.html", form=form, user=user)

        user.name      = form.name.data
        user.email     = form.email.data
        user.login     = form.login.data
        user.superuser = form.superuser.data
        if len(form.password.data) > 0:
            user.password = form.password.data
        db.session().commit()

        return redirect(url_for("users_index"))

    elif request.method == "DELETE":
        db.session().delete(user)
        db.session().commit()
        return ""
    




# Edit user profile
@app.route("/profile", methods=["GET", "POST"])
@login_required
def users_profile_edit():
    if request.method == "GET":
        form = UserEditForm(obj=current_user)
        return render_template("users/edit_profile.html", form=form, user=current_user)

    else:
        form = UserEditForm(request.form)

        if not form.validate():
            return render_template("users/edit_profile.html", form=form, user=current_user)

        current_user.name      = form.name.data
        current_user.email     = form.email.data
        current_user.login     = form.login.data
        if len(form.password.data) > 0:
            current_user.password = form.password.data
        db.session().commit()

        return redirect(url_for("index"))


