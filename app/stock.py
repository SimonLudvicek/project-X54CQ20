from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
import yfinance as yf
import pandas as pd
from . import db

class Stock(Model):
    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=0)  
    purchase_price = Column(Float, default=0.0)  
    user_id = Column(Integer, nullable=False)  
    
    exchange_rate = 0.85  

    def get_stock_data(self):
        if self.quantity is None:
            self.quantity = 0
        if self.purchase_price is None:
            self.purchase_price = 0.0
        if self.user_id is None:
            self.user_id = 1  

        data = yf.download(self.symbol, start="2023-01-01", end="2023-12-1")
        data.reset_index(inplace=True)

        data['Close_EUR'] = data['Close'] * self.exchange_rate

        return data.to_dict(orient='records')

class AppleStock(Model):
    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=0)
    purchase_price = Column(Float, default=0.0)
    user_id = Column(Integer, nullable=False)

    exchange_rate = 0.85  

    def get_stock_data(self):
        if self.quantity is None:
            self.quantity = 0
        if self.purchase_price is None:
            self.purchase_price = 0.0
        if self.user_id is None:
            self.user_id = 1

        data = yf.download(self.symbol, start="2022-01-01", end="2023-01-01")
        data.reset_index(inplace=True)

        data['Close_EUR'] = data['Close'] * self.exchange_rate

        return data.to_dict(orient='records')