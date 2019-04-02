from application                 import app, db, login_required
from application.products.models import Product
from application.homes.models    import Home
from flask                       import redirect, render_template, url_for
from flask_login                 import current_user


@app.route("/reports", methods=["GET"])
@login_required()
def reports_index():
    class Report(object):
        def __init__(self, id, name, description):
            self.id          = id
            self.name        = name
            self.description = description

    reports = [ Report("best_before", "Best before", "List items past or nearing the best before -date.") ]
    homes = current_user.get_my_homes()
    return render_template("reports/index.html", reports=reports, homes=homes)


@app.route("/reports/<report_id>/<home_id>", methods=["GET"])
@login_required()
def report_show(report_id, home_id):
    home = Home.query.get(home_id)
    if report_id == "best_before":
        days = 7
        items = home.get_stock_going_bad(days)
        return render_template("reports/best_before.html", home=home, items=items, days=days)
    else:
        return redirect(url_for("reports_index"))

