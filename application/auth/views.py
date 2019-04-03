from flask                    import render_template, request, redirect, url_for
from flask_login              import current_user, login_user, logout_user, login_required
from application              import app, db
from application.users.models import User
from application.auth.forms   import PasswordChangeForm, LoginForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    else:
        form = LoginForm(request.form)

        user = User.query.filter_by(login = form.login.data).first()
        if not user or not user.check_password(form.password.data):
            return render_template("auth/loginform.html", form = form, error = "No such username or password.")

        login_user(user)
        return redirect(url_for("index"))

@app.route("/auth/logout", methods = ["GET"])
@login_required
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/unauthorized", methods = ["GET"])
def auth_unauthorized():
    return render_template("auth/unauthorized.html")


# Password changing:
@app.route("/auth/change_password", methods=["GET", "POST"])
@login_required
def auth_change_password():
    if not current_user:
        return redirect(url_for("index"))
    
    if request.method == "GET":
        return render_template("auth/change_password.html", form = PasswordChangeForm())
    else:
        form = PasswordChangeForm(request.form)

        if not form.validate():
            return render_template("auth/change_password.html", form = form)

        current_user.change_password(form.password.data)
        current_user.force_password_change = False
        db.session().commit()
        
        return redirect(url_for("index"))

