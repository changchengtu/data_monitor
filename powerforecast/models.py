# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100L)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128L)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(max_length=30L, unique=True)
    first_name = models.CharField(max_length=30L)
    last_name = models.CharField(max_length=30L)
    email = models.CharField(max_length=75L)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = 'auth_user'

class BacktestOutput(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(null=True, blank=True)
    value = models.DecimalField(null=True, max_digits=18, decimal_places=3, blank=True)
    location = models.CharField(max_length=4L, blank=True)
    backtest_date = models.DateField(null=True, blank=True)
    weather = models.IntegerField(null=True, blank=True)
    hydro = models.IntegerField(null=True, blank=True)
    nuke = models.IntegerField(null=True, blank=True)
    stateburndaily = models.DecimalField(decimal_places=3, null=True, max_digits=18, db_column='StateBurnDaily', blank=True) # Field name made lowercase.
    error = models.DecimalField(null=True, max_digits=18, decimal_places=4, blank=True)
    trade_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'backtest_output'

class Commentary(models.Model):
    id = models.IntegerField(primary_key=True)
    subject = models.CharField(max_length=45L, blank=True)
    content = models.TextField(blank=True)
    author_id = models.IntegerField(null=True, blank=True)
    publish_datetime = models.DateTimeField(null=True, blank=True)
    edit_datetime = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'commentary'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200L)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L)
    app_label = models.CharField(max_length=100L)
    model = models.CharField(max_length=100L)
    class Meta:
        db_table = 'django_content_type'

class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)
    app = models.CharField(max_length=255L)
    name = models.CharField(max_length=255L)
    applied = models.DateTimeField()
    class Meta:
        db_table = 'django_migrations'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100L)
    name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'django_site'

class ForecastOutput(models.Model):
    date = models.DateField(null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=63L, blank=True)
    forecast_date = models.CharField(max_length=63L, blank=True)
    weather = models.BigIntegerField(null=True, blank=True)
    hydro = models.BigIntegerField(null=True, blank=True)
    nuke = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'forecast_output'

class RegionalMonthlyIndex(models.Model):
    region = models.TextField(blank=True)
    date = models.DateTimeField(blank=True, null=True)
    year = models.BigIntegerField(blank=True, null=True)
    month = models.BigIntegerField(blank=True, null=True)
    average = models.FloatField(blank=True, null=True)
    number_2std_high = models.FloatField(db_column='2std_high', blank=True, null=True) # Field renamed because it wasn't a valid Python identifier.
    number_2std_low = models.FloatField(db_column='2std_low', blank=True, null=True) # Field renamed because it wasn't a valid Python identifier.
    median = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        # managed = False
        db_table = 'regional_monthly_index'

class SouthMigrationhistory(models.Model):
    id = models.IntegerField(primary_key=True)
    app_name = models.CharField(max_length=255L)
    migration = models.CharField(max_length=255L)
    applied = models.DateTimeField()
    class Meta:
        db_table = 'south_migrationhistory'

class UsMonthlyIndex(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    year_x = models.BigIntegerField(blank=True, null=True)
    month = models.BigIntegerField(blank=True, null=True)
    median = models.FloatField(blank=True, null=True)
    year_y = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'us_monthly_index'

class UsDailyIndex(models.Model):
    date = models.DateField(blank=True, null=True)
    month = models.BigIntegerField(blank=True, null=True)
    day = models.BigIntegerField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    eia_value = models.FloatField(blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'us_daily_index'

class WeatherScenario(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(null=True, blank=True)
    weather_analogue_year = models.CharField(max_length=45L, db_column='Weather_Analogue_Year', blank=True) # Field name made lowercase.
    value = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'weather_scenario'

class FcchangeTable(models.Model):
    region = models.CharField(max_length=63L, blank=True)
    date = models.CharField(max_length=63L, blank=True)
    year = models.BigIntegerField(null=True, blank=True)
    month = models.BigIntegerField(null=True, blank=True)
    current = models.FloatField(null=True, blank=True)
    lastmonth = models.FloatField(null=True, blank=True)
    change_lastmonth = models.FloatField(null=True, blank=True)
    lastweek = models.FloatField(null=True, blank=True)
    change_lastweek = models.FloatField(null=True, blank=True)
    current_f = models.CharField(max_length=63L, blank=True)
    lastmonth_f = models.CharField(max_length=63L, blank=True)
    change_lastmonth_f = models.CharField(max_length=63L, blank=True)
    lastweek_f = models.CharField(max_length=63L, blank=True)
    change_lastweek_f = models.CharField(max_length=63L, blank=True)
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        db_table = 'fcchange_table'

class NeartermTable(models.Model):
    date = models.TextField(blank=True)
    thisyear = models.TextField(db_column='thisYear', blank=True, null=True) # Field name made lowercase.
    lastyear = models.TextField(db_column='lastYear', blank=True, null=True) # Field name made lowercase.
    yoy = models.TextField(db_column='YoY', blank=True, null=True) # Field name made lowercase.
    east_thisyear = models.TextField(db_column='East_thisYear', blank=True) # Field name made lowercase.
    east_lastyear = models.TextField(db_column='East_lastYear', blank=True) # Field name made lowercase.
    east_yoy = models.TextField(db_column='East_YoY', blank=True) # Field name made lowercase.
    midwest_thisyear = models.TextField(db_column='Midwest_thisYear', blank=True) # Field name made lowercase.
    midwest_lastyear = models.TextField(db_column='Midwest_lastYear', blank=True) # Field name made lowercase.
    midwest_yoy = models.TextField(db_column='Midwest_YoY', blank=True) # Field name made lowercase.
    mountain_thisyear = models.TextField(db_column='Mountain_thisYear', blank=True) # Field name made lowercase.
    mountain_lastyear = models.TextField(db_column='Mountain_lastYear', blank=True) # Field name made lowercase.
    mountain_yoy = models.TextField(db_column='Mountain_YoY', blank=True) # Field name made lowercase.
    pacific_thisyear = models.TextField(db_column='Pacific_thisYear', blank=True) # Field name made lowercase.
    pacific_lastyear = models.TextField(db_column='Pacific_lastYear', blank=True) # Field name made lowercase.
    pacific_yoy = models.TextField(db_column='Pacific_YoY', blank=True) # Field name made lowercase.
    south_central_thisyear = models.TextField(db_column='South Central_thisYear', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    south_central_lastyear = models.TextField(db_column='South Central_lastYear', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    south_central_yoy = models.TextField(db_column='South Central_YoY', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'nearterm_table'

class WheelActual(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    pipe_30_avg = models.FloatField(blank=True, null=True)
    temp_30_avg = models.FloatField(blank=True, null=True)
    price_30_avg = models.FloatField(blank=True, null=True)
    forecast_30_avg = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'wheel_actual'

class ForecastMonthly(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=63, blank=True)
    average = models.FloatField(blank=True, null=True)
    number_2std_high = models.FloatField(db_column='2std_high', blank=True, null=True) # Field renamed because it wasn't a valid Python identifier.
    number_2std_low = models.FloatField(db_column='2std_low', blank=True, null=True) # Field renamed because it wasn't a valid Python identifier.
    median = models.FloatField(blank=True, null=True)
    forecast_date = models.CharField(max_length=63, blank=True)
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'forecast_monthly'

class EiaDaily(models.Model):
    date = models.DateField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    location = models.TextField(blank=True)
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'eia_daily'

class RiskForecastStdTable(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    std_low = models.FloatField(blank=True, null=True)
    median = models.FloatField(blank=True, null=True)
    std_high = models.FloatField(blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'risk_forecast_std_table'