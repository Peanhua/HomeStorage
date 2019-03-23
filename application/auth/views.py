from flask                    import render_template, request, redirect, url_for
from flask_login              import login_user, logout_user, login_required
from application              import app
from application.users.models import User
from application.auth.forms   import LoginForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    else:
        form = LoginForm(request.form)

        user = User.query.filter_by(login = form.login.data, password = form.password.data).first()
        if not user:
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
