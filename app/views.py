import calendar
import logging

from flask_appbuilder.charts.views import (
    DirectByChartView, DirectChartView, GroupByChartView
)
from flask_appbuilder.models.group import aggregate_avg, aggregate_sum
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView

from . import appbuilder
from .models import Country, CountryStats, PoliticalType, Portfolio

log = logging.getLogger(__name__)

class PortfolioView(ModelView):
    datamodel = SQLAInterface(Portfolio)
    

class CountryStatsModelView(ModelView):
    datamodel = SQLAInterface(CountryStats)
    list_columns = ["country", "stat_date", "population", "unemployed", "college"]


class CountryModelView(ModelView):
    datamodel = SQLAInterface(Country)


class PoliticalTypeModelView(ModelView):
    datamodel = SQLAInterface(PoliticalType)


class CountryStatsDirectChart(DirectChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = "Statistics"
    chart_type = "LineChart"
    direct_columns = {
        "General Stats": ("stat_date", "population", "unemployed", "college")
    }
    base_order = ("stat_date", "asc")


def pretty_month_year(value):
    return calendar.month_name[value.month] + " " + str(value.year)


class CountryDirectChartView(DirectByChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = "Direct Data"

    definitions = [
        {
            "group": "stat_date",
            "series": ["unemployed", "college"],
        }
    ]


class CountryGroupByChartView(GroupByChartView):
    datamodel = SQLAInterface(CountryStats)
    chart_title = "Statistics"

    definitions = [
        {
            "label": "Country Stat",
            "group": "country",
            "series": [
                (aggregate_avg, "unemployed"),
                (aggregate_avg, "population"),
                (aggregate_avg, "college"),
            ],
        },
        {
            "group": "month_year",
            "formatter": pretty_month_year,
            "series": [
                (aggregate_sum, "unemployed"),
                (aggregate_avg, "population"),
                (aggregate_avg, "college"),
            ],
        },
    ]


appbuilder.add_view(
    CountryModelView, "List Countries", icon="fa-folder-open-o", category="Statistics"
)
appbuilder.add_view(
    PoliticalTypeModelView,
    "List Political Types",
    icon="fa-folder-open-o",
    category="Statistics",
)
appbuilder.add_view(
    CountryStatsModelView,
    "List Country Stats",
    icon="fa-folder-open-o",
    category="Statistics",
)
appbuilder.add_separator("Statistics")
appbuilder.add_view(
    CountryStatsDirectChart,
    "Show Country Chart",
    icon="fa-dashboard",
    category="Statistics",
)
appbuilder.add_view(
    CountryGroupByChartView,
    "Group Country Chart",
    icon="fa-dashboard",
    category="Statistics",
)
appbuilder.add_view(
    CountryDirectChartView,
    "Show Country Chart",
    icon="fa-dashboard",
    category="Statistics",
)
appbuilder.add_view(
    PortfolioView,
    "Show Portfolio",
    icon="fa-folder-open-o",
    category="Statistics"
)

from flask_appbuilder import BaseView, SimpleFormView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask import render_template, flash
from . import appbuilder, db
from .news import NewsModel, NewsForm

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
        # post process form
        flash(self.message, "info")

appbuilder.add_view(
    NewsListView,
    "List News",
    icon="fa-cogs",
    label="News List",
    category="News",
    category_icon="fa-group",
)

appbuilder.add_view(
    NewsView,
    "News View",
    icon="fa-cogs",
    label=("Add News"),
    category="News",
    category_icon="fa-group",
)

from .portfolio import Stock, MyUser

class StockModelView(ModelView):
    datamodel = SQLAInterface(Stock)
    list_columns = ['symbol', 'name', 'quantity', 'purchase_price', 'user.username']

class UserModelView(ModelView):
    datamodel = SQLAInterface(MyUser)
    related_views = [StockModelView]

appbuilder.add_view(StockModelView, 
                    "List Stocks", 
                    icon="fa-table", 
                    category="Portfolio",
                    category_icon="fa-folder-open-o")

appbuilder.add_view(UserModelView, 
                    "List Users", 
                    icon="fa-user", 
                    category="Portfolio")

db.create_all()

