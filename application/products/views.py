from application import app, db
from application.products.models import Product
from flask import redirect, render_template, request, url_for

# List of products
@app.route("/products", methods=["GET"])
def products_index():
    return render_template("products/list.html", products = Product.query.all())


# Create new product
@app.route("/products/new/")
def products_form():
    return render_template("products/new.html")

@app.route("/products/", methods=["POST"])
def products_create():
    product = Product(request.form.get("name"))

    db.session().add(product)
    db.session().commit()
    
    return redirect(url_for("products_index"))


@app.route("/products/<product_id>/", methods=["POST"])
def products_update(product_id):
    product = Product.query.get(product_id)
    product.name = request.form.get("name")
    print(request.form.get("name"))
    db.session().commit()

    return redirect(url_for("products_index"))
