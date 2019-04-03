from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField, validators

class LoginForm(FlaskForm):
    login    = StringField("Login:")
    password = PasswordField("Password:")

    class Meta:
        csrf = False



class PasswordChangeForm(FlaskForm):
    password = PasswordField("Password:", [validators.DataRequired(), validators.Length(min=8)])

    class Meta:
        csrf = False
