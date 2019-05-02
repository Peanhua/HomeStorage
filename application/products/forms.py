from flask_wtf import FlaskForm
from wtforms   import IntegerField, StringField, validators

class ProductForm(FlaskForm):
    name             = StringField("Name:", [validators.DataRequired(), validators.Length(min=4, max=80)])
    default_lifetime = IntegerField("Default lifetime:", default=14, validators=[validators.DataRequired(), validators.NumberRange(min=1, max=36500)])
