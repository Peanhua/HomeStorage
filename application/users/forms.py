from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField

class UserForm(FlaskForm):
    name     = StringField("Name:")
    email    = StringField("Email:")
    login    = StringField("Login:")
    password = PasswordField("Password:")

    class Meta:
        csrf = False
