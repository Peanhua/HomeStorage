from application              import app, db
from application.homes.models import Home
from application.homes.forms  import HomeForm
from flask                    import redirect, render_template, request, url_for
from flask_login              import login_required

# List of homes
@app.route("/homes", methods=["GET"])
@login_required
def homes_index():
    return render_template("homes/list.html", homes = Home.query.all())


# Create new home
@app.route("/homes/new/")
@login_required
def homes_form():
    return render_template("homes/new.html", form = HomeForm())

@app.route("/homes/", methods=["POST"])
@login_required
def homes_create():
    form = HomeForm(request.form)

    if not form.validate():
        return render_template("homes/new.html", form = form)
    
    home = Home(form.name.data)

    db.session().add(home)
    db.session().commit()
    
    return redirect(url_for("homes_index"))
