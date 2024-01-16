from flask_appbuilder import Model
from flask import request
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from flask_login import UserMixin
from wtforms import StringField, FloatField, IntegerField, SelectField
from wtforms.validators import InputRequired, NumberRange, ValidationError
from flask_appbuilder.forms import DynamicForm
from enum import Enum
from . import db

class StockSymbols(Enum):
    AAPL = 'AAPL'
    TSLA = 'TSLA'
    MSFT = 'MSFT'
    AMZN = 'AMZN'

class StockForm(DynamicForm):
    symbol_choices = [(symbol.value, symbol.name) for symbol in StockSymbols]
    
    symbol = SelectField('Symbol', choices=symbol_choices, validators=[InputRequired()])
    name = StringField('Name')
    price = FloatField('Price', default=0.0)
    quantity = IntegerField('Quantity', default=0)

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        # Volá se před standardní validací a umožňuje úpravy formuláře
        if obj:
            self.name.data = self.get_stock_name(StockSymbols(obj.symbol))
        super().process(formdata, obj, data, **kwargs)

    def validate(self, extra_validators=None):
        # Validace a doplnění jména akcie podle vybraného symbolu
        if not super().validate():
            return False

        selected_symbol = StockSymbols(self.symbol.data)
        self.name.data = self.get_stock_name(selected_symbol)

        return True

    def get_stock_name(self, symbol):
        # Logika pro získání jména akcie podle vybraného symbolu
        if symbol == StockSymbols.AAPL:
            return 'Apple Inc.'
        elif symbol == StockSymbols.TSLA:
            return 'Tesla, Inc.'
        elif symbol == StockSymbols.MSFT:
            return 'Microsoft Corporation'
        elif symbol == StockSymbols.AMZN:
            return 'Amazon.com, Inc.'
        else:
            return ''

class SellStockForm(DynamicForm):
    price = IntegerField('Sell Price', validators=[InputRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=1)])

    def validate_quantity(form, field):
        if 'items' in request.form:
            # Získáme seznam akcií ze žádosti
            item_ids = request.form.get('items').split(',')
            items = [db.session.query(Stock).get(int(item_id)) for item_id in item_ids]

            # Kontrola, zda uživatel nemá na skladě méně akcií, než chce prodat
            for item in items:
                if item.quantity < field.data:
                    raise ValidationError('You do not have enough stocks to sell.')

class MyUser(Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    extended_user_id = Column(Integer, ForeignKey('extended_user.id'))
    
class Stock(Model):
    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, default=0.0)
    quantity = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('my_user.id'))

class ExtendedUser(Model):
    id = Column(Integer, primary_key=True)
    my_user_id = Column(Integer, ForeignKey('my_user.id'))