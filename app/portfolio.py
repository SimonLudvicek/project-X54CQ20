from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Stock(Model):
    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('ab_user.id'))
    user = relationship("MyUser", primaryjoin="foreign(Stock.user_id) == MyUser.id")

class MyUser(Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    stocks = relationship("Stock", primaryjoin="foreign(Stock.user_id) == MyUser.id")