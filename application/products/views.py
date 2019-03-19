from application import app, db
from application.products.models import Product
from flask import redirect, render_template, request, url_for

@app.route("/products", methods=["GET"])
def products_index():
    return render_template("products/list.html", products = Product.query.all())


@app.route("/products/new/")
def products_form():
    return render_template("products/new.html")

@app.route("/products/", methods=["POST"])
def products_create():
    product = Product(request.form.get("name"))

    db.session().add(product)
    db.session().commit()
    
    return redirect(url_for("products_index"))
