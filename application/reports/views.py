from application                 import app, db, login_required
from application.products.models import Product
from application.homes.models    import Home
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

    reports = [ Report("best_before", "Best before", "List items past or nearing the best before -date.", "Days", 7) ]
    homes = current_user.get_my_homes()
    return render_template("reports/index.html", reports=reports, homes=homes)


@app.route("/reports/<report_id>/<home_id>/<param1>", methods=["GET"])
@login_required()
def report_show(report_id, home_id, param1):
    home = Home.query.get(home_id)
    if report_id == "best_before":
        days = int(param1)
        items = home.get_stock_going_bad(days)
        return render_template("reports/best_before.html", home=home, items=items, days=days)
    else:
        return redirect(url_for("reports_index"))

