from flask_wtf import FlaskForm
from wtforms   import FormField, FieldList, HiddenField, IntegerField, StringField, validators

class HomeForm(FlaskForm):
    name = StringField("Name:", [validators.DataRequired(), validators.Length(min=4, max=80)])

    class Meta:
        csrf = False

class MyHomeProductForm(FlaskForm):
    product_id   = HiddenField("Product ID", [validators.Optional()])
    product_name = HiddenField("Product", [validators.Optional()])
    mindesired   = IntegerField("Min desired quantity", [validators.Optional()])
    maxdesired   = IntegerField("Max desired quantity", [validators.Optional()])

class MyHomeForm(FlaskForm):
    products = FieldList(FormField(MyHomeProductForm))

    class Meta:
        csrf = False
