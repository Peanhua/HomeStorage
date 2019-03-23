import os

import dotenv
dotenv.load_dotenv()

from flask import Flask
app = Flask(__name__)


# Setup database connection:
from flask_sqlalchemy import SQLAlchemy

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///homestorage.db"
    app.config["SQLALCHEMY_ECHO"] = True
    
# The next is to silence this warning: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Wrap login_required:
from functools   import wraps
from flask_login import current_user
from flask       import redirect, url_for

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            unauthorized = False

            if role != "ANY":
                unauthorized = True

                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break

                if unauthorized:
                    return redirect(url_for("auth_unauthorized")) #login_manager.unauthorized()

            return fn(*args, **kwargs)
            
        return decorated_view
    return wrapper




# Authentication
secretkey = os.environ.get("SECRET_KEY")
if not secretkey:
    secretkey = os.urandom(32)
app.config["SECRET_KEY"] = secretkey

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."



# Load application content:
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



# Authentication continued:
from application.users.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Initialize database:
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
