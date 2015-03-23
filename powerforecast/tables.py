import django_tables2 as tables
from powerforecast.models import *

class BacktestOutputTable(tables.Table):
    class Meta:
        model = BacktestOutput
        # add class="paleblue" to <table> tag
        attrs = {"class": "table table-striped table-bordered table-hover dataTables-example"}