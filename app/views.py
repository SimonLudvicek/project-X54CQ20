import logging


from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView

from . import appbuilder, db
from flask_appbuilder import ModelView, SimpleFormView, expose, BaseView
from flask import flash, url_for, redirect, request
from .news import NewsModel, NewsForm
from .stock import SapStock, AppleStock, TeslaStock, MicrosoftStock, AmazonStock
from flask_appbuilder.actions import action
from flask_login import current_user
from .portfolio import Stock, StockForm, SellStockForm


log = logging.getLogger(__name__)
 
#Novinky

class NewsListView(BaseView):
    default_view = "list_news"

    @expose("/list/")
    def list_news(self):
        news_list = db.session.query(NewsModel).all()
        return self.render_template(
            "news_list.html", news_list=news_list, base_template="appbuilder/base.html"
        )
    
class NewsView(SimpleFormView):
    form = NewsForm
    form_title = "Enter some exciting news"
    message = "Your news were submitted"

    def form_post(self, form):
        if form.validate_on_submit():
            news_entry = NewsModel(
                title=form.title.data,
                date=form.date.data,
                text=form.text.data
            )
            db.session.add(news_entry)
            db.session.commit()
            flash(self.message, "info")
        else:
            flash("Formulář není platný.", "warning")
    
    @expose("/show/<int:news_id>/", methods=["GET"])
    def news_detail(self, news_id):
        news_entry = db.session.query(NewsModel).get(news_id)
        if news_entry:
            return self.render_template(
                "news_detail.html", news_entry=news_entry, base_template="appbuilder/base.html"
            )
        else:
            flash("Zpráva s ID {} nebyla nalezena.".format(news_id), "warning")

appbuilder.add_view(
    NewsListView,
    "List News",
    icon="fa-info-circle",
    label="News List",
    category="News",
    category_icon="fa-newspaper",
)

appbuilder.add_view(
    NewsView,
    "News View",
    icon="fa-bell",
    label=("Add News"),
    category="News",
    category_icon="fa-newspaper",
)

#Nákup a prodej akcií

class StockModelView(ModelView):
    datamodel = SQLAInterface(Stock)
    list_columns = ['symbol', 'name', 'quantity', 'price']
    show_columns = ['symbol', 'name', 'quantity', 'price']

    @action("sell", "Sell", "Do you really want to sell this stock?")
    def action_sell(self, items):
        return redirect(url_for('.sell_stock', ids=','.join(str(item.id) for item in items)))

    @expose('/sell_stock/', methods=['GET', 'POST'])
    def sell_stock(self):
        form = SellStockForm(request.form)
        item_ids = request.args.get('ids').split(',')
        items = [self.datamodel.get(int(item_id)) for item_id in item_ids]

        if request.method == 'POST' and form.validate():
            total_earnings = 0

            for item in items:
                if item.quantity < form.quantity.data:
                    flash('You do not have enough stocks to sell.', 'warning')
                    return redirect(url_for('.sell_stock', ids=request.args.get('ids')))

                earnings = (form.price.data - item.price) * form.quantity.data
                total_earnings += earnings

                db.session.delete(item)

            db.session.commit()
            flash(f'Stock sold successfuly! Total Earnings/Loss: {total_earnings}', 'info')
            return redirect(url_for('StockModelView.list'))

        return self.render_template('sell_stock.html', form=form, items=items)

class StockFormView(SimpleFormView):
    form = StockForm
    form_title = 'Buy Stock'
    form_template = 'appbuilder/general/model/edit.html'
    message = 'Stock bought successfully.'

    def form_post(self, form):
        existing_stock = db.session.query(Stock).filter_by(symbol=form.symbol.data, user_id=current_user.id).first()
        if existing_stock:
            existing_stock.quantity += form.quantity.data
            existing_stock.price = form.price.data
        else:
            stock = Stock()
            stock.symbol = form.symbol.data
            stock.name = form.name.data
            stock.quantity = form.quantity.data
            stock.price = form.price.data

            stock.user = current_user

            db.session.add(stock)

        db.session.commit()
        flash(self.message, 'info')

        return redirect(url_for('StockModelView.list'))

appbuilder.add_view(
    StockModelView,
    "My Stocks",
    icon="fa-wallet",
    category="Portfolio",
    category_icon="fa-bank"
)

appbuilder.add_view(
    StockFormView,
    "Buy Stock",
    icon="fa-dollar-sign",
    category="Portfolio",
)

#Zobrazování grafů

class StockGraphView(BaseView):
    default_view = "sap_stock_graph"

    @expose("/sap_stock_graph/")
    def sap_stock_graph(self):
        sap_stock = db.session.query(SapStock).filter_by(symbol="^GSPC").first()
        if sap_stock is None:
            default_user_id = 1 
            sap_stock = SapStock(symbol="^GSPC", name="S&P 500", user_id=default_user_id)
            db.session.add(sap_stock)
            db.session.commit()

        stock_data = sap_stock.get_stock_data()
        return self.render_template(
            "sap_graph.html", stock_data=stock_data, base_template="appbuilder/base.html"
        )

class AppleStockGraphView(BaseView):
    default_view = "apple_stock_graph"

    @expose("/apple_stock_graph/")
    def apple_stock_graph(self):
        apple_stock = db.session.query(AppleStock).filter_by(symbol="AAPL").first()
        if apple_stock is None:
            default_user_id = 1  
            apple_stock = AppleStock(symbol="AAPL", name="Apple Inc.", user_id=default_user_id)
            db.session.add(apple_stock)
            db.session.commit()

        stock_data = apple_stock.get_stock_data()
        return self.render_template(
            "apple_graph.html", stock_data=stock_data, base_template="appbuilder/base.html"
        )

class TeslaStockGraphView(BaseView):
    default_view = "tesla_stock_graph"

    @expose("/tesla_stock_graph/")
    def tesla_stock_graph(self):
        tesla_stock = db.session.query(TeslaStock).filter_by(symbol="TSLA").first()
        if tesla_stock is None:
            default_user_id = 1  
            tesla_stock = TeslaStock(symbol="TSLA", name="Tesla Inc.", user_id=default_user_id)
            db.session.add(tesla_stock)
            db.session.commit()

        stock_data = tesla_stock.get_stock_data()
        return self.render_template(
            "tesla_graph.html", stock_data=stock_data, base_template="appbuilder/base.html"
        )

class MicrosoftStockGraphView(BaseView):
    default_view = "microsoft_stock_graph"

    @expose("/microsoft_stock_graph/")
    def microsoft_stock_graph(self):
        microsoft_stock = db.session.query(MicrosoftStock).filter_by(symbol="MSFT").first()
        if microsoft_stock is None:
            default_user_id = 1  
            microsoft_stock = MicrosoftStock(symbol="MSFT", name="Microsoft Corporation", user_id=default_user_id)
            db.session.add(microsoft_stock)
            db.session.commit()

        stock_data = microsoft_stock.get_stock_data()
        return self.render_template(
            "microsoft_graph.html", stock_data=stock_data, base_template="appbuilder/base.html"
        )
    
class AmazonStockGraphView(BaseView):
    default_view = "amazon_stock_graph"

    @expose("/amazon_stock_graph/")
    def amazon_stock_graph(self):
        amazon_stock = db.session.query(AmazonStock).filter_by(symbol="AMZN").first()
        if amazon_stock is None:
            default_user_id = 1  
            amazon_stock = AmazonStock(symbol="AMZN", name="Amazon.com Inc.", user_id=default_user_id)
            db.session.add(amazon_stock)
            db.session.commit()

        stock_data = amazon_stock.get_stock_data()
        return self.render_template(
            "amazon_graph.html", stock_data=stock_data, base_template="appbuilder/base.html"
        )
    

appbuilder.add_view(
    StockGraphView,
    "S&P 500 Graph",
    icon="fa-line-chart",
    category="Stocks",
    category_icon="fa-money",
)

appbuilder.add_view(
    AppleStockGraphView,
    "Apple Stock Graph",
    icon="fa-line-chart",
    category="Stocks",
    category_icon="fa-money",
)

appbuilder.add_view(
    TeslaStockGraphView,
    "Tesla Stock Graph",
    icon="fa-line-chart",
    category="Stocks",
    category_icon="fa-money",
)

appbuilder.add_view(
    MicrosoftStockGraphView,
    "Microsoft Stock Graph",
    icon="fa-line-chart",
    category="Stocks",
    category_icon="fa-money",
)

appbuilder.add_view(
    AmazonStockGraphView,
    "Amazon Stock Graph",
    icon="fa-line-chart",
    category="Stocks",
    category_icon="fa-money",
)

db.create_all()

