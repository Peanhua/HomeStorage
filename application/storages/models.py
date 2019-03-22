from application import db

class Storage(db.Model):
    storage_id = db.Column(db.Integer,    primary_key = True)
    home_id    = db.Column(db.Integer,    db.ForeignKey("home.home_id"), nullable = False)
    name       = db.Column(db.String(80),                                nullable = False)

    def __init__(self, home_id, name):
        self.home_id = home_id
        self.name    = name
