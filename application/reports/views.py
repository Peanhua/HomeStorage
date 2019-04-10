from application                 import app, db, login_required
from application.products.models import Product
from application.homes.models    import Home
#from application.reports.forms   import ReportsForm
from flask                       import redirect, render_template, url_for
from flask_login                 import current_user


@app.route("/reports", methods=["GET"])
@login_required()
def reports_index():
    class Report(object):
        def __init__(self, id, name, description, param1label, param1default):
            self.id            = id
            self.name          = name
            self.description   = description
            self.param1label   = param1label
            self.param1default = param1default

    reports = [
        Report("best_before",      "Best before",      "List items past or nearing the best before -date.",      "Days", 7   ),
        Report("missing_products", "Missing products", "List products whose quantity is below minimum desired.", None,   None)
    ]
    homes = current_user.get_my_homes()
    #form.best_before_home.choices = [(h.home_id, h.name) for h in homes]
    #form.missing_products_home.choices = [(h.home_id, h.name) for h in homes]
    return render_template("reports/index.html", reports=reports, homes=homes)


@app.route("/reports/<report_id>/<home_id>/<param1>", methods=["GET"])
@login_required()
def report_show(report_id, home_id, param1):
    home = Home.query.get(home_id)
    if not home.is_user_in(current_user.user_id):
        return redirect(url_for("auth_unauthorized"))
    
    if report_id == "best_before":
        try:
            days = int(param1)
        except:
            days = 0
        if days < 0:
            days = 0
        if days > 365:
            days = 365
        items = home.get_stock_going_bad(days)
        return render_template("reports/best_before.html", home=home, items=items, days=days)
    elif report_id == "missing_products":
        products = home.get_stock_missing()
        return render_template("reports/missing_products.html", home=home, products=products)
    else:
        return redirect(url_for("reports_index"))

