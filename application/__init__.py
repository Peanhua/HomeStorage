from flask import Flask
app = Flask(__name__)


from flask_sqlaclhemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///homestorage.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


from application import views


db.create_all()
