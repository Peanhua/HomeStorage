from application.users.models import User
from flask_wtf                import FlaskForm
from wtforms                  import BooleanField, HiddenField, PasswordField, StringField, validators, ValidationError

def check_unique_login(form, field):
    existing = User.query.filter(User.user_id != form.user_id.data, User.login == field.data).first()
    if existing:
        raise ValidationError("This login is already in use, please choose another.")


class UserBaseForm(FlaskForm):
    user_id   = HiddenField("User ID",     [validators.Optional()])
    name      = StringField("Name:",       [validators.DataRequired(), validators.Length(min=4, max=80)])
    email     = StringField("Email:",      [validators.DataRequired(), validators.Length(min=8, max=80), validators.Email()])
    login     = StringField("Login:",      [validators.DataRequired(), validators.Length(min=4, max=40), check_unique_login])

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
