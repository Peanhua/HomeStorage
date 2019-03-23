from application              import db
from application.homes.models import Home

class User(db.Model):

    # Change the name of the table because "user" is a restricted keyword in PostgreSQL:
    __tablename__ = "account"
    
    user_id   = db.Column(db.Integer,    primary_key = True)
    name      = db.Column(db.String(80), nullable = False)
    login     = db.Column(db.String(40), nullable = False)
    password  = db.Column(db.String(40), nullable = False)
    email     = db.Column(db.String(80), nullable = False)
    superuser = db.Column(db.Boolean,    nullable = False)

    homes = db.relationship("HomeUser", back_populates="user", cascade="all, delete, delete-orphan")
    #homes = db.relationship("HomeUser", backref="user", cascade="all, delete, delete-orphan")

    def __init__(self, name, email, login, password):
        self.name      = name
        self.email     = email
        self.login     = login
        self.password  = password
        self.superuser = False

    def get_id(self):
        return self.user_id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        if self.superuser:
            return ["ADMIN"]
        else:
            return ["USER"]

    def get_my_homes(self):
        myhomes = [home.home_id for home in self.homes]
        return Home.query.filter(Home.home_id.in_(myhomes)).order_by("name").all()
