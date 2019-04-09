from application                 import app, login_required
from application.homes.models    import Home
from application.products.models import Product
from application.users.models    import User
from flask                       import render_template
from flask_login                 import current_user

@app.route("/")
@login_required()
def index():
    if "ADMIN" in current_user.roles():
        systemstatus = {
            "homes":    Home.query.all(),
            "products": Product.query.all(),
            "users":    User.query.all(),
        }

    return render_template("index.html", systemstatus=systemstatus)

@app.route("/docs/")
def docs_index():
    with open("application/static/docs/index.css") as fp:
        css = fp.read()
    with open("application/static/docs/index.md") as fp:
        content = fp.read()
    return render_template("doc.html", css=css, content=content)


@app.route("/docs/<name>.png")
def docs_png(name):
    return app.send_static_file("docs/" + name + ".png")
