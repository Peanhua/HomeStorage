from flask_wtf import FlaskForm
from wtforms   import StringField, SelectField, validators

class StorageForm(FlaskForm):
    home = SelectField("Home:", [validators.DataRequired()], coerce=int)
    name = StringField("Name:", [validators.DataRequired(), validators.Length(min=4, max=40)])

    class Meta:
        csrf = False


class StorageEditForm(FlaskForm):
    name = StringField("Name:", [validators.DataRequired(), validators.Length(min=4, max=40)])
    class Meta:
        csrf = False


class StorageDeleteForm(FlaskForm):
    class Meta:
        csrf = False

