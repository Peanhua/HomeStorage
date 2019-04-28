from application                 import app, login_required
from application.homes.models    import Home
from application.items.models    import Item
from application.products.models import Product
from application.storages.models import Storage
from application.users.models    import User
from flask                       import redirect, render_template, url_for
from flask_login                 import current_user
import os

@app.route("/")
@login_required()
def index():
    myhomes = current_user.get_my_homes().all()
    for home in myhomes:
        setattr(home, "bad_stock", home.get_stock_going_bad(3))
        setattr(home, "missing_products", home.get_stock_missing())
        setattr(home, "storages", Storage.query.filter(Storage.home_id == home.home_id).all())

    if "ADMIN" in current_user.roles():
        systemstatus = {
            "homes":     Home.query.all(),
            "products":  Product.query.all(),
            "users":     User.query.all(),
            "itemcount": Item.get_total()
        }
    else:
        systemstatus = { }

    return render_template("index.html", myhomes=myhomes, systemstatus=systemstatus)


@app.route("/docs/")
def docs_index():
    return docs_md("index")

@app.route("/docs/<name>.png")
def docs_png(name):
    return app.send_static_file("documentation/" + name + ".png")

@app.route("/docs/<name>.md")
def docs_md(name):
    if name.find("/") != -1:
        return redirect(url_for("auth_unauthorized"))
    
    filename = "documentation/" + name + ".md"
    if not os.path.isfile(filename):
        return redirect(url_for("auth_unauthorized"))
    
    with open("documentation/index.css") as fp:
        css = fp.read()
    with open(filename) as fp:
        content = fp.read()
    return render_template("doc.html", css=css, content=content)
    
