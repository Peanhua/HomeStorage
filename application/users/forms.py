from flask_wtf import FlaskForm
from wtforms   import BooleanField, PasswordField, StringField, validators

class UserBaseForm(FlaskForm):
    name      = StringField("Name:",       [validators.DataRequired(), validators.Length(min=4, max=80)])
    email     = StringField("Email:",      [validators.DataRequired(), validators.Length(min=8, max=80), validators.Email()])
    login     = StringField("Login:",      [validators.DataRequired(), validators.Length(min=4, max=40)])

    class Meta:
        csrf = False

class UserNewForm(UserBaseForm):
    password  = PasswordField("Password:", [validators.DataRequired(), validators.Length(min=8)])
    superuser = BooleanField("Superuser:", [validators.Optional()])

class UserEditForm(UserBaseForm):
    password  = PasswordField("Password:", [validators.Optional(), validators.Length(min=8)])
    superuser = BooleanField("Superuser:", [validators.Optional()])

class UserProfileForm(UserBaseForm):
    password  = PasswordField("Password:", [validators.Optional(), validators.Length(min=8)])
