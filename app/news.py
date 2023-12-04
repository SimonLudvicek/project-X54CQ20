from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Date
from . import db

class NewsModel(Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    text = Column(String, nullable=False)

class NewsForm(DynamicForm):
    title = StringField(
        ("Title"),
        description=("Enter title"),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
    )
    date = DateField(
        "Date", description="Enter the date", validators=[DataRequired()]
    )
    text = TextAreaField(
        ("Text"), description=("Enter long text"), widget=BS3TextFieldWidget()
    )
    
