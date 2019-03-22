from flask_wtf import FlaskForm
from wtforms   import StringField, PasswordField, validators

class UserForm(FlaskForm):
    name     = StringField("Name:",       [validators.DataRequired(), validators.Length(min=4, max=80)])
    email    = StringField("Email:",      [validators.DataRequired(), validators.Length(min=8, max=80), validators.Email()])
    login    = StringField("Login:",      [validators.DataRequired(), validators.Length(min=4, max=40)])
    password = PasswordField("Password:", [validators.DataRequired(), validators.Length(min=8)])

    class Meta:
        csrf = False
