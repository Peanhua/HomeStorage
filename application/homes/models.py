from application import db

class Home(db.Model):
    home_id  = db.Column(db.Integer,    primary_key = True)
    name     = db.Column(db.String(80), nullable = False)

    def __init__(self, name):
        self.name     = name


class HomeUser(db.Model):
    homeuser_id = db.Column(db.Integer, primary_key = True)
    home_id     = db.Column(db.Integer, db.ForeignKey("home.home_id"),    nullable = False)
    user_id     = db.Column(db.Integer, db.ForeignKey("account.user_id"), nullable = False)

    def __init__(self, home_id, user_id):
        self.home_id = home_id
        self.user_id = user_id

