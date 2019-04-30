from application                 import app, db, login_required, get_items_per_page
from application.homes.models    import Home, HomeUser, HomeProduct
from application.homes.forms     import HomeForm, MyHomeForm
from application.users.models    import User
from application.products.models import Product
from flask                       import redirect, render_template, request, url_for
from flask_login                 import current_user
from flask_sqlalchemy            import Pagination

# List of homes
@app.route("/homes/", methods=["GET"], defaults={"page": 1})
@app.route("/homes/<int:page>", methods=["GET"])
@login_required(role="ADMIN")
def homes_index(page):
    return render_template("homes/list.html", homes = Home.query.paginate(page=page, per_page=get_items_per_page()))


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
    
    return redirect(url_for("homeusers_edit", home_id=home.home_id))


# Delete home
@app.route("/homes/<home_id>/delete", methods=["GET", "DELETE"])
@login_required(role="ADMIN")
def homes_delete(home_id):
    home = Home.query.get(home_id)
    if not home:
        return redirect(url_for("auth_unauthorized"))

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
    if not home:
        return redirect(url_for("auth_unauthorized"))
    
    if request.method == "GET":
        form = HomeForm()
        form.name.data = home.name
        return render_template("homes/edit.html", form=form, home=home)

    else:
        form = HomeForm(request.form)

        if not form.validate():
            return render_template("homes/edit.html", form=form, home=home)

        home.name = form.name.data
        db.session().commit()
        return redirect(url_for("homes_index"))



# Home users editing:
@app.route("/homes/users/<home_id>/", methods=["GET", "POST"])
@login_required(role="ADMIN")
def homeusers_edit(home_id):
    home = Home.query.get(home_id)
    if not home:
        return redirect(url_for("auth_unauthorized"))
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
@app.route("/myhomes/", methods=["GET"], defaults={"page": 1})
@app.route("/myhomes/<int:page>", methods=["GET"])
@login_required()
def myhomes_index(page):
    homes = current_user.get_my_homes().paginate(page=page, per_page=get_items_per_page())
    return render_template("homes/mylist.html", homes = homes)

# My Homes editing:
@app.route("/myhomes/<home_id>/", methods=["GET", "POST"])
@login_required()
def myhomes_edit(home_id):
    home = Home.query.get(home_id)
    if not home:
        return redirect(url_for("auth_unauthorized"))

    if not home.is_user_in(current_user.user_id):
        return redirect(url_for("auth_unauthorized"))

    if request.method == "GET":
        res = home.get_products()

        class Foo(object):
            def __init__(self, products):
                self.products = products
        form = MyHomeForm(obj=Foo(res))
        
        return render_template("homes/myedit.html", home=home, form=form)

    else:
        form = MyHomeForm(request.form)

        if not form.validate():
            return render_template("homes/myedit.html", home=home, form=form)

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
@app.route("/myhomes/view/<home_id>/", methods=["GET"], defaults={"users_page": 1})
@app.route("/myhomes/view/<home_id>/", methods=["GET"], defaults={"products_page": 1})
@app.route("/myhomes/view/<home_id>/", methods=["GET"], defaults={"users_page": 1, "products_page": 1})
@app.route("/myhomes/view/<home_id>/<int:users_page>/<int:products_page>", methods=["GET"])
@login_required()
def myhomes_view(home_id, users_page, products_page):
    home = Home.query.get(home_id)
    if not home:
        return redirect(url_for("auth_unauthorized"))

    if not home.is_user_in(current_user.user_id):
        return redirect(url_for("auth_unauthorized"))
    
    homeuserids = [ u.user_id for u in home.users]
    homeusers   = User.query.filter(User.user_id.in_(homeuserids)).paginate(page=users_page, per_page=get_items_per_page())

    stock = home.get_stock(page=products_page, per_page=get_items_per_page())
    products = Pagination(None, page=products_page, per_page=get_items_per_page(), total=Product.query.count(), items=stock)
    return render_template("homes/myview.html", home=home, homeusers=homeusers, products=products)
