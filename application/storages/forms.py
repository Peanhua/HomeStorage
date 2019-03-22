from flask_wtf import FlaskForm
from wtforms   import StringField, validators

class StorageForm(FlaskForm):
    name = StringField("Name:", [validators.DataRequired(), validators.Length(min=4, max=40)])

    class Meta:
        csrf = False
