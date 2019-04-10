from application                 import app, db, login_required
from application.homes.models    import Home, HomeUser, HomeProduct
from application.homes.forms     import HomeForm, MyHomeForm
from application.users.models    import User
from application.products.models import Product
from flask                       import redirect, render_template, request, url_for
from flask_login                 import current_user

# List of homes
@app.route("/homes", methods=["GET"])
@login_required(role="ADMIN")
def homes_index():
    homes = Home.query.all()
    return render_template("homes/list.html", homes = homes)


# Create new home
@app.route("/homes/new/")
@login_required(role="ADMIN")
def homes_form():
    return render_template("homes/new.html", form = HomeForm())

@app.route("/homes/", methods=["POST"])
@login_required(role="ADMIN")
def homes_create():
    form = HomeForm(request.form)

    if not form.validate():
        return render_template("homes/new.html", form = form)
    
    home = Home(form.name.data)

    db.session().add(home)
    db.session().commit()
    
    return redirect(url_for("homes_index"))


# Delete home
@app.route("/homes/<home_id>/delete", methods=["GET", "DELETE"])
@login_required(role="ADMIN")
def homes_delete(home_id):
    home = Home.query.get(home_id)
    if request.method == "GET":
        stock = home.get_stock_items()
        return render_template("homes/delete.html", home=home, stock=stock)
    elif request.method == "DELETE":
        home.delete()
        return url_for("homes_index")



# Edit home
@app.route("/homes/<home_id>/", methods=["GET", "POST"])
@login_required(role="ADMIN")
def homes_edit(home_id):
    home = Home.query.get(home_id)
    
    if request.method == "GET":
        form = HomeForm()
        form.name.data = home.name
        return render_template("homes/edit.html", form=form, home=home)

    else:
        form = HomeForm(request.form)

        if not form.validate():
            return render_template("homes/edit.html", form = form)

        home.name = form.name.data
        db.session().commit()
        return redirect(url_for("homes_index"))



# Home users editing:
@app.route("/homes/users/<home_id>/", methods=["GET", "POST"])
@login_required(role="ADMIN")
def homeusers_edit(home_id):
    home = Home.query.get(home_id)
    homeuserids = [ u.user_id for u in home.users]
    
    homeusers  = User.query.filter(User.user_id.in_(homeuserids)).all()
    otherusers = User.query.filter(~User.user_id.in_(homeuserids)).all()
    
    if request.method == "GET":
        return render_template("homes/edit_users.html", home=home, homeusers=homeusers, otherusers=otherusers)

    elif request.method == "POST":
        # Delete HomeUsers not in saveduids, and add new HomeUsers for those that didn't exist before:
        saveduids = [int(uid) for uid in request.form.getlist("homeusers")]
        
        for hu in home.users:
            if hu.user_id not in saveduids:
                db.session().delete(hu)
            else:
                saveduids.remove(hu.user_id)

        for uid in saveduids:
            homeuser = HomeUser(home.home_id, uid)
            db.session().add(homeuser)

        db.session().commit()
        
        return redirect(url_for("homes_index"))



# My Homes list:
@app.route("/myhomes", methods=["GET"])
@login_required()
def myhomes_index():
    homes = current_user.get_my_homes()
    return render_template("homes/mylist.html", homes = homes)

# My Homes editing:
@app.route("/myhomes/<home_id>/", methods=["GET", "POST"])
@login_required()
def myhomes_edit(home_id):
    home = Home.query.get(home_id)
    # TODO: check that current_user has permission to edit the home

    if request.method == "GET":
        res = home.get_products()

        class Foo(object):
            def __init__(self, products):
                self.products = products
        form = MyHomeForm(obj=Foo(res))
        
        return render_template("homes/myedit.html", home=home, form=form)

    else:
        form = MyHomeForm(request.form)

        #if not form.validate():
        #    return render_template("homes/myedit.html", home=home, form=form)

        # Delete and add new... TODO: fix this to update (where applicable) ?
        HomeProduct.query.filter(HomeProduct.home_id == home.home_id).delete()
        for product in form.products.data:
            product_id = int(product["product_id"])
            mindesired = int(product["mindesired"])
            maxdesired = int(product["maxdesired"])
            if mindesired > 0 or maxdesired > 0:
                hp = HomeProduct(home.home_id, product_id, mindesired, maxdesired)
                db.session().add(hp)
        
        db.session().commit()
        return redirect(url_for("myhomes_index"))



# View my home:
@app.route("/myhomes/view/<home_id>/", methods=["GET"])
@login_required()
def myhomes_view(home_id):
    home = Home.query.get(home_id)
    
    homeuserids = [ u.user_id for u in home.users]
    homeusers   = User.query.filter(User.user_id.in_(homeuserids)).all()

    if current_user.user_id not in homeuserids:
        return redirect(url_for("myhomes_index"));

    products = home.get_stock_all()

    return render_template("homes/myview.html", home=home, homeusers=homeusers, products=products)
