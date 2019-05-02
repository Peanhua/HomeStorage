from flask_wtf import FlaskForm
from wtforms   import IntegerField, SelectField, validators

class ReportsForm(FlaskForm):
    best_before_home = SelectField("Home:", [validators.DataRequired()], coerce=int)
    best_before_days = IntegerField("Days", [validators.InputRequired(), validators.NumberRange(min=0, max=365)])
    missing_products_home = SelectField("Home:", [validators.DataRequired()], coerce=int)
