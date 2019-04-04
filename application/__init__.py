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

# Turn on foreign keys for sqlite:
from sqlalchemy.engine import Engine
from sqlalchemy        import event
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

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

            if role != "ANY":
                if role not in current_user.roles():
                    return redirect(url_for("auth_unauthorized"))

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

from application.items    import models

from application.reports  import views


# Authentication continued:
from application.users.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Handle forced password changes:
from flask import request
@app.before_request
def force_password_change():
    if not current_user:
        return None
    if current_user.is_authenticated:
        if current_user.force_password_change:
            if request.path != url_for("auth_change_password") and request.path != url_for("auth_logout"):
                return redirect(url_for("auth_change_password"))


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
