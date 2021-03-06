from application              import app, db, login_required, get_items_per_page
from application.users.models import User
from application.users.forms  import UserNewForm, UserEditForm, UserProfileForm
from flask                    import abort, redirect, render_template, request, url_for
from flask_login              import current_user

# List of users
@app.route("/users/", methods=["GET"], defaults={"page": 1})
@app.route("/users/<int:page>", methods=["GET"])
@login_required(role="ADMIN")
def users_index(page):
    users = User.query.order_by(User.name).paginate(page=page, per_page=get_items_per_page(), error_out=False)
    if users.page > 1 and users.page > users.pages:
        return redirect(url_for("users_index"))
    return render_template("users/list.html", users=users)


# Create new user
@app.route("/users/new/")
@login_required(role="ADMIN")
def users_form():
    return render_template("users/new.html", form = UserNewForm())

@app.route("/users/", methods=["POST"])
@login_required(role="ADMIN")
def users_create():
    form = UserNewForm(request.form)

    if not form.validate():
        return render_template("users/new.html", form = form)
    
    user = User(form.name.data,
                form.email.data,
                form.login.data,
                form.password.data)

    user.superuser = form.superuser.data
    user.force_password_change = True
    
    db.session().add(user)
    db.session().commit()
    
    return redirect(url_for("users_index"))


# Edit user
@app.route("/users/<user_id>/", methods=["GET", "POST", "DELETE"])
@login_required(role="ADMIN")
def users_edit(user_id):
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for("auth_unauthorized"))

    if request.method == "GET":
        form = UserEditForm(obj=user)
        return render_template("users/edit.html", form=form, user=user)

    elif request.method == "POST":
        form = UserEditForm(request.form)

        if not form.validate():
            return render_template("users/edit.html", form=form, user=user)

        user.name                  = form.name.data
        user.email                 = form.email.data
        user.login                 = form.login.data
        user.superuser             = form.superuser.data
        user.force_password_change = form.force_password_change.data
        if len(form.password.data) > 0:
            user.change_password(form.password.data)
        db.session().commit()

        return redirect(url_for("users_index"))

    elif request.method == "DELETE":
        if user.user_id == 1:
            return abort(400, "Root user can not be deleted.")
        
        if user.user_id == current_user.user_id:
            return abort(400, "Unable to delete the current user.")
        
        db.session().delete(user)
        db.session().commit()
        return ""
    




# Edit user profile
@app.route("/profile", methods=["GET", "POST"])
@login_required()
def users_profile_edit():
    if request.method == "GET":
        form = UserProfileForm(obj=current_user)
        return render_template("users/edit_profile.html", form=form, user=current_user)

    else:
        form = UserProfileForm(request.form)

        if not form.validate():
            return render_template("users/edit_profile.html", form=form, user=current_user)

        current_user.name  = form.name.data
        current_user.email = form.email.data
        if len(form.password.data) > 0:
            current_user.change_password(form.password.data)
        db.session().commit()

        return redirect(url_for("index"))


