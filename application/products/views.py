from application                 import app, db
from application.products.models import Product
from application.products.forms  import ProductForm
from flask                       import redirect, render_template, request, url_for

# List of products
@app.route("/products", methods=["GET"])
def products_index():
    return render_template("products/list.html", products = Product.query.all())


# Create new product
@app.route("/products/new/")
def products_form():
    return render_template("products/new.html", form = ProductForm())

@app.route("/products/", methods=["POST"])
def products_create():
    form = ProductForm(request.form)

    if not form.validate():
        return render_template("products/new.html", form = form)
    
    product = Product(form.name.data)

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
