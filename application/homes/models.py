from application                 import is_sqlite
from application                 import db
from application.products.models import Product
from sqlalchemy.sql              import text
from sqlalchemy                  import and_, or_

class Home(db.Model):
    home_id  = db.Column(db.Integer,    primary_key = True)
    name     = db.Column(db.String(80), nullable = False)

    users = db.relationship("HomeUser", backref="home", lazy=True)

    def __init__(self, name):
        self.name = name


    def is_user_in(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return True
        return False
        
    def delete(self):
        q = text("DELETE FROM home WHERE home_id = :home_id").params(home_id=self.home_id)
        res = db.engine.execute(q)
        db.session().commit()
        res.close()
        
    def get_products(self):
        res = db.session().query(Product, HomeProduct).outerjoin(HomeProduct, and_(Product.product_id == HomeProduct.product_id,
                                                                                   or_(HomeProduct.home_id == self.home_id,
                                                                                       HomeProduct.home_id.is_(None)))).order_by(Product.name).all()
        class TmpProduct(object):
            def __init__(self, product_id, name, mind, maxd):
                self.product_id   = product_id
                self.product_name = name
                self.mindesired   = mind
                self.maxdesired   = maxd
        fps = []
        for i in res:
            product = i[0]
            hprod   = i[1]
            mind = getattr(hprod, "desired_min_quantity", 0)
            maxd = getattr(hprod, "desired_max_quantity", 0)
            fps.append(TmpProduct(product.product_id, product.name, mind, maxd))

        return fps;

    def get_stock_items(self):
        q = text(
            "SELECT product.product_id AS product_id,"
            "       product.name       AS product_name,"
            "       SUM(item.quantity) AS current_quantity"
            "  FROM product"
            "  LEFT OUTER JOIN home_product ON product.product_id = home_product.product_id"
            "  LEFT OUTER JOIN item         ON product.product_id = item.product_id"
            "                              AND item.storage_id IN ( SELECT storage.storage_id"
            "                                                         FROM storage"
            "                                                        WHERE storage.home_id = :home_id )"
            " GROUP BY product.product_id"
            " HAVING current_quantity > 0"
        ).params(home_id=self.home_id)
        res = db.engine.execute(q)
        rv = []
        for row in res:
            rv.append({"product_id":       row[0],
                       "product_name":     row[1],
                       "current_quantity": row[2] if row[2] else 0
                       })
        res.close()
        return rv
    
    def get_stock(self, only_missing=False, page=None, per_page=None):
        sql = "" \
            "SELECT home_product.product_id           AS product_id," \
            "       t.product_name                    AS product_name," \
            "       home_product.desired_min_quantity AS desired_min_quantity," \
            "       home_product.desired_max_quantity AS desired_max_quantity," \
            "       t.current_quantity                AS current_quantity" \
            "  FROM ( SELECT product.product_id AS product_id," \
            "                product.name       AS product_name," \
            "                SUM(item.quantity) AS current_quantity" \
            "           FROM product" \
            "           LEFT OUTER JOIN home_product ON product.product_id = home_product.product_id" \
            "                                           AND ( home_product.home_id = :home_id OR home_product.home_id IS NULL)" \
            "           LEFT OUTER JOIN item ON product.product_id = item.product_id" \
            "                                   AND item.storage_id IN ( SELECT storage.storage_id" \
            "                                                              FROM storage" \
            "                                                             WHERE storage.home_id = :home_id )" \
            "          GROUP BY product.product_id" \
            "        ) t" \
            "  LEFT JOIN home_product ON home_product.product_id = t.product_id" \
            "                        AND home_product.home_id = :home_id"

        if only_missing:
            sql += \
                " WHERE current_quantity < desired_min_quantity" \
                "    OR (current_quantity IS NULL AND desired_min_quantity IS NOT NULL)"

        sql += " ORDER BY t.product_name"

        if page and per_page:
            sql += " LIMIT " + str(per_page) + " OFFSET " + str((page - 1) * per_page)

        q = text(sql).params(home_id=self.home_id)
        res = db.engine.execute(q)
        
        rv = []
        for row in res:
            rv.append({"product_id":           row[0],
                       "product_name":         row[1],
                       "desired_min_quantity": row[2] if row[2] else 0,
                       "desired_max_quantity": row[3] if row[3] else 0,
                       "current_quantity":     row[4] if row[4] else 0
                       })
        res.close()
        return rv

    def get_stock_missing(self):
        return self.get_stock(True)
    

    def get_stock_going_bad(self, days):
        # name, storage, best_before, days_remaining
        if is_sqlite():
            q = text("SELECT product.name     AS name,"
                     "       item.quantity    AS quantity,"
                     "       storage.name     AS storage,"
                     "       item.best_before AS best_before,"
                     "       JULIANDAY(item.best_before) - JULIANDAY(date()) AS days_remaining"
                     "  FROM item"
                     "  JOIN product ON product.product_id = item.product_id"
                     "  JOIN storage ON storage.storage_id = item.storage_id"
                     " WHERE storage.home_id = :home_id"
                     "   AND days_remaining < :days"
                     " ORDER BY days_remaining"
            ).params(home_id=self.home_id, days=days)
        else:
            # PostgreSQL:
            q = text("SELECT *"
                     "  FROM ( SELECT product.name      AS name,"
                     "                item.quantity     AS quantity,"
                     "                storage.name      AS storage,"
                     "                item.best_before  AS best_before,"
                     "                CAST(TO_CHAR(item.best_before, 'J') AS INT) - CAST(TO_CHAR(now(), 'J') AS INT) AS days_remaining"
                     "           FROM item"
                     "           JOIN product ON product.product_id = item.product_id"
                     "           JOIN storage ON storage.storage_id = item.storage_id"
                     "          WHERE storage.home_id = :home_id"
                     "       ) tmp"
                     " WHERE days_remaining < :days"
                     " ORDER BY days_remaining"
            ).params(home_id=self.home_id, days=days)
            
        res = db.engine.execute(q)
        rv = []
        for row in res:
            rv.append({"name":           row[0],
                       "quantity":       row[1],
                       "storage":        row[2],
                       "best_before":    row[3],
                       "days_remaining": int(row[4])
                       })
        res.close()
        return rv



class HomeUser(db.Model):
    homeuser_id = db.Column(db.Integer, primary_key = True)
    home_id     = db.Column(db.Integer, db.ForeignKey("home.home_id", ondelete="CASCADE"),    nullable = False, index = True)
    user_id     = db.Column(db.Integer, db.ForeignKey("account.user_id", ondelete="CASCADE"), nullable = False, index = True)

    user = db.relationship("User")

    def __init__(self, home_id, user_id):
        self.home_id = home_id
        self.user_id = user_id


class HomeProduct(db.Model):
    homeproduct_id       = db.Column(db.Integer, primary_key = True)
    home_id              = db.Column(db.Integer, db.ForeignKey("home.home_id", ondelete="CASCADE"),       nullable = False, index = True)
    product_id           = db.Column(db.Integer, db.ForeignKey("product.product_id", ondelete="CASCADE"), nullable = False, index = True)
    desired_min_quantity = db.Column(db.Integer, nullable = True)
    desired_max_quantity = db.Column(db.Integer, nullable = True)

    def __init__(self, home_id, product_id, desired_min_quantity, desired_max_quantity):
        self.home_id              = home_id
        self.product_id           = product_id
        self.desired_min_quantity = desired_min_quantity
        self.desired_max_quantity = desired_max_quantity
