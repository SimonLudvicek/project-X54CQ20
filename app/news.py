from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired


class News(DynamicForm):
    field1 = StringField(
        ("Field1"),
        description=("Enter title"),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
    )
    field2 = DateField(
        "Field2", description="Enter the date", validators=[DataRequired()]
    )
    field3 = TextAreaField(
        ("Field3"), description=("Enter long text"), widget=BS3TextFieldWidget()
    )
    
