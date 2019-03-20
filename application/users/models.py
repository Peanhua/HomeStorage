from application import db

class User(db.Model):
    id       = db.Column(db.Integer,    primary_key = True)
    name     = db.Column(db.String(80), nullable = False)
    login    = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(80), nullable = False)

    def __init__(self, name, login, password):
        self.name     = name
        self.login    = login
        self.password = password
