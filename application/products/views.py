from application                 import app, db
from application.products.models import Product
from application.products.forms  import ProductForm
from application.items.models    import Item
from flask                       import redirect, render_template, request, url_for, abort
from flask_login                 import login_required
from sqlalchemy                  import exc

# List of products
@app.route("/products", methods=["GET"])
@login_required
def products_index():
    return render_template("products/list.html", products = Product.query.all())


# Create new product
@app.route("/products/new/")
@login_required
def products_form():
    return render_template("products/new.html", form = ProductForm())

@app.route("/products/", methods=["POST"])
@login_required
def products_create():
    form = ProductForm(request.form)

    if not form.validate():
        return render_template("products/new.html", form = form)
    
    product = Product(form.name.data, form.default_lifetime.data)

    db.session().add(product)
    db.session().commit()
    
    return redirect(url_for("products_index"))


# Edit product
@app.route("/products/<product_id>/", methods=["GET", "POST", "DELETE"])
@login_required
def products_edit(product_id):
    product = Product.query.get(product_id)
    if not product:
        return redirect(url_for("auth_unauthorized"))

    if request.method == "GET":
        form = ProductForm(obj=product)
        return render_template("products/edit.html", form=form, product=product)

    elif request.method == "POST":
        form = ProductForm(request.form)

        if not form.validate():
            return render_template("products/edit.html", form=form, product=product)

        product.name = request.form.get("name")
        product.default_lifetime = request.form.get("default_lifetime")
        db.session().commit()

        return redirect(url_for("products_index"))

    elif request.method == "DELETE":
        try:
            db.session().delete(product)
            db.session().commit()
            return "", 204
        except exc.SQLAlchemyError:
            db.session().rollback()
            itemcount = Item.query.filter(Item.product_id == product.product_id).count()
            if itemcount > 0:
                return "Unable to delete product '" + product.name + "', it is in use by " + str(itemcount) + " items.", 405
            else:
                abort(418)
