from application.users.models import User
from flask_wtf                import FlaskForm
from wtforms                  import BooleanField, HiddenField, PasswordField, StringField, validators, ValidationError

def check_unique_login(form, field):
    if form.user_id.data:
        uid = int(form.user_id.data)
    else:
        uid = -1
    existing = User.query.filter(User.user_id != uid, User.login == field.data).first()
    if existing:
        raise ValidationError("This login is already in use, please choose another.")


class UserBaseForm(FlaskForm):
    user_id   = HiddenField("User ID",     [validators.Optional()])
    name      = StringField("Name:",       [validators.DataRequired(), validators.Length(min=4, max=80)])
    email     = StringField("Email:",      [validators.DataRequired(), validators.Length(min=8, max=80), validators.Email()])

class UserNewForm(UserBaseForm):
    login     = StringField("Login:",      [validators.DataRequired(), validators.Length(min=4, max=40), check_unique_login])
    password  = PasswordField("Password:", [validators.DataRequired(), validators.Length(min=8)])
    superuser = BooleanField("Superuser:", [validators.Optional()])

class UserEditForm(UserBaseForm):
    login                 = StringField("Login:",                  [validators.DataRequired(), validators.Length(min=4, max=40), check_unique_login])
    password              = PasswordField("Password:",             [validators.Optional(),     validators.Length(min=8)])
    superuser             = BooleanField("Superuser:",             [validators.Optional()])
    force_password_change = BooleanField("Force password change:", [validators.Optional()])

class UserProfileForm(UserBaseForm):
    password  = PasswordField("Password:", [validators.Optional(), validators.Length(min=8)])
