from flask import Flask
app = Flask(__name__)


from flask_sqlalchemy import SQLAlchemy
import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///homestorage.db"
    app.config["SQLALCHEMY_ECHO"] = True
    
# The next is to silence this warning: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


from application          import views

from application.auth     import views

from application.products import models
from application.products import views

from application.storages import models
from application.storages import views

from application.users    import models
from application.users    import views

from application.homes    import models
from application.homes    import views



# Authentication
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

from application.users.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()
except:
    pass

# Create default root user:
root = load_user(1)
if not root:
    root = User("Superuser", "root@not.set.invalid", "root", "root")
    root.superuser = True
    db.session().add(root)
    db.session().commit()
