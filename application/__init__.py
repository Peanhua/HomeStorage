from flask import Flask
app = Flask(__name__)


from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///homestorage.db"
app.config["SQLALCHEMY_ECHO"] = True
# The next is to silence this warning: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


from application import views

from application.products import models
from application.products import views

db.create_all()
