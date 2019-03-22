from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField

class LoginForm(FlaskForm):
    login    = StringField("Login:")
    password = PasswordField("Password:")

    class Meta:
        csrf = False
