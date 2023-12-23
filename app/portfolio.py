from flask import flash
from flask_appbuilder import Model, BaseView, expose
from flask_appbuilder.models.mixins import AuditMixin
from flask_appbuilder.models.decorators import renders
from flask_appbuilder.forms import DynamicForm
from wtforms import SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import appbuilder, db


class MyUser(Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    stocks = relationship("Stock", primaryjoin="foreign(Stock.user_id) == MyUser.id")

class Portfolio(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ab_user.id'))
    user = relationship("MyUser", primaryjoin="foreign(Portfolio.user_id) == MyUser.id")
    stock_type = Column(String(50), nullable=False)
    stock_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    sale_price = Column(Float)

class PortfolioForm(DynamicForm):
    stock_type = SelectField("Stock Type", choices=[], validators=[DataRequired()])
    stock_id = SelectField("Stock", choices=[], validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    purchase_price = DecimalField("Purchase Price", validators=[DataRequired()])

