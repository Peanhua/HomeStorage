from flask_wtf import FlaskForm
from wtforms   import StringField, validators

class ProductForm(FlaskForm):
    name = StringField("Name:", [validators.DataRequired(), validators.Length(min=4, max=80)])

    class Meta:
        csrf = False
