from application import db

class User(db.Model):

    # Change the name of the table because "user" is a restricted keyword in PostgreSQL:
    __tablename__ = "account"
    
    id        = db.Column(db.Integer,    primary_key = True)
    name      = db.Column(db.String(80), nullable = False)
    login     = db.Column(db.String(40), nullable = False)
    password  = db.Column(db.String(40), nullable = False)
    email     = db.Column(db.String(80), nullable = False)
    superuser = db.Column(db.Boolean,    nullable = False)

    def __init__(self, name, email, login, password):
        self.name      = name
        self.email     = email
        self.login     = login
        self.password  = password
        self.superuser = False

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
