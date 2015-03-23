import os
import inspect
import MySQLdb
import json
import pandas as pd
from datetime import datetime, date, timedelta
import urllib, urllib2, cookielib
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
import time

server_url = "eia.cwvrtrnm3ga3.us-west-2.rds.amazonaws.com"
db = MySQLdb.connect(server_url,"observ","forecast123" )
mysql_cnxn = create_engine('mysql+mysqldb://observ:forecast123@eia.cwvrtrnm3ga3.us-west-2.rds.amazonaws.com:3306')

def eiaMoni():
	print 'eiaMoni is running'
	url = 'http://api.eia.gov/series/?api_key=45780D1A92A4F363815C75600ACF5748&series_id=NG.N3045AL2.M'
	api_data = json.load(urllib2.urlopen(url))

	latest_eia_sql = ('select max(date) FROM eiadev.eia_data')
	updated_date = pd.read_sql(latest_eia_sql,db)['max(date)'][0]

	latest_date_eiaWebsite = api_data["series"][0]["data"][0][0]
	latest_value_eiaWebsite = api_data["series"][0]["data"][0][1]

	report = {}
	conclude = False
	message = ''
	message += 'The latest update day: '+str(updated_date)+'\n'
	message += 'EIA website has updated data in '+str(latest_date_eiaWebsite)+'\n'
	if str(latest_value_eiaWebsite) == 'NA' :
		conclude = True
		message += 'But the part we need has not been updated yet, please check:'+'\n'
		message += 'http://api.eia.gov/series/?api_key=45780D1A92A4F363815C75600ACF5748&series_id=NG.N3045AL2.M'
	elif str(latest_date_eiaWebsite)!=str(updated_date):
		conclude = False
	else:
		conclude = True


	report['updated_date']=updated_date
	report['conclude']=conclude
	report['message']=message

	return report



def priceForwardMoni():
	print 'priceForwardMoni is running'
	latest_rows_sql = 'SELECT file_date, COUNT(*) FROM pricedev.price_forward WHERE file_date = (SELECT MAX(file_date) FROM pricedev.price_forward)'
	rows_data = pd.read_sql(latest_rows_sql,db)

	hubs_eachState_sql = 'SELECT contract, file_date, COUNT(location) FROM pricedev.price_forward WHERE file_date = (SELECT  MAX(file_date) FROM pricedev.price_forward) GROUP BY 1 '
	hubs_data = pd.read_sql(hubs_eachState_sql, db)

	updated_date = rows_data['file_date'][0]
	num_rows = rows_data['COUNT(*)'][0]

	hubs_correct = True
	for num in hubs_data['COUNT(location)']:
		if num<70:
			hubs_correct=False

	rows_correct = True
	if num_rows>7000:
		rows_correct = True
	else:
		rows_correct = False

	## total state
	report = {}
	message=''
	conclude = False
	if datetime.today().date()-timedelta(days=3) <= updated_date:
		if hubs_correct==True and rows_correct==True:
			conclude = True

	message += 'The latest update day: '+str(updated_date)+'\n'
	if hubs_correct == True:
		message += 'Number of hubs each state is 70, correct\n'
	else:
		message += 'Number of hubs each state is not correct\n'

	if rows_correct:
		message += 'Inserted '+str(num_rows)+' rows, it seems okay because it more than 7,000\n'
	else:
		message += 'Inserted less than 7,000, please check it again...\n'

	
	report['updated_date']=updated_date
	report['message']=message
	report['conclude']=conclude
	report['num_rows']=num_rows

	return report


def priceCashMoni():
	print 'priceCashMoni is running'
	latest_rows_sql = 'SELECT issue_date, COUNT(*) FROM pricedev.price_cash WHERE issue_date = (SELECT MAX(issue_date) FROM pricedev.price_cash)'
	rows_data = pd.read_sql(latest_rows_sql,db)

	updated_date = rows_data['issue_date'][0]
	num_rows = rows_data['COUNT(*)'][0]

	rows_correct = True
	if num_rows==145:
		rows_correct = True
	else:
		rows_correct = False

	## total state
	report={}
	conclude = False
	if datetime.today().date()-timedelta(days=3) <= updated_date:
		if rows_correct ==True:
			conclude = True

	message = ''
	message += 'The latest update day is: '+str(updated_date)+'\n'
	if rows_correct:
		message += 'Inserted '+str(num_rows)+' rows, okay!\n'

	else:
		message += 'Inserted '+str(num_rows)+' rows, please check it again...\n'

	report['updated_date']=updated_date
	report['conclude']=conclude
	report['message']=message
	report['num_rows']=num_rows
	
	return report


def priceMonthlyAvgMoni():
	print 'priceMonthlyAvgMoni'
	latest_locs_sql = ('SELECT year, month, count(*) FROM pricedev.price_cash_monthly_average '
						'WHERE month = (SELECT MAX(month) FROM (SELECT * FROM pricedev.price_cash_monthly_average WHERE year = (SELECT MAX(year) FROM pricedev.price_cash_monthly_average)) AS monthly_average) '
        					'AND year = (SELECT MAX(year) FROM pricedev.price_cash_monthly_average)')
	locs_data = pd.read_sql(latest_locs_sql,db)

	updated_date = date(locs_data['year'],locs_data['month'],1)
	num_locs = locs_data['count(*)'][0]

	report={}
	conclude = False
	if datetime.today().date().month == updated_date.month:
		if num_locs == 37:
			conclude = True

	message=''
	message += 'The latest update day is: '+str(updated_date)+'\n'

	report['updated_date']=updated_date
	report['conclude']=conclude
	report['message']=message
	report['num_locs']=num_locs

	return report




def tempActMoni():
	print 'tempActMoni'
	latest_wbans_sql = ('SELECT date,count(*) FROM weatherdev.weather_actual WHERE date = (SELECT  MAX(date) FROM (SELECT  * FROM weatherdev.weather_actual WHERE Tavg is not NULL) as actual);')
	wbans_data = pd.read_sql(latest_wbans_sql,db)

	updated_date = wbans_data['date'][0]
	num_wbans = wbans_data['count(*)'][0]

	## total state
	report={}
	conclude = False
	if num_wbans>230:
		conclude = True

	message = ''
	message += 'The latest update day: '+str(updated_date)+'\n'
	message += str(num_wbans)+' wbans have been updated! \n'

	report['updated_date']=updated_date
	report['conclude']=conclude
	report['message']=message
	report['num_wbans']=num_wbans

	return report
	


def tempForeMoni():
	print 'tempForeMoni'
	latest_wbans_sql = ('SELECT forecast_date, count(*) FROM weatherdev.weather_forecast WHERE forecast_date = (SELECT  MAX(forecast_date) FROM weatherdev.weather_forecast);')
	wbans_data = pd.read_sql(latest_wbans_sql,db)

	updated_date = wbans_data['forecast_date'][0]
	num_wbans = wbans_data['count(*)'][0]

	yesterday_wbans_sql = ('SELECT forecast_date, count(*) FROM weatherdev.weather_forecast WHERE forecast_date = (SELECT MAX(forecast_date) FROM weatherdev.weather_forecast where forecast_date<'+'"'+str(wbans_data['forecast_date'][0])+'")')
	yesterday_wbans_data = pd.read_sql(yesterday_wbans_sql,db)
	yesterday_num_wbans = yesterday_wbans_data['count(*)'][0]
	yesterday = yesterday_wbans_data['forecast_date'][0]

	report={}
	conclude = False
	if str(yesterday) == str(datetime.today().date()-timedelta(days=1)):
		if int(yesterday_num_wbans) == 3960:
			conclude = True

	message = ''
	message += 'The latest update day: '+str(updated_date)+'\n'
	message += str(num_wbans)+' wbans have been updated today!\n'
	message += str(yesterday_num_wbans)+ ' wbans have been updated on '+str(yesterday)+'\n'

	report['updated_date']=updated_date
	report['conclude']=conclude
	report['message']=message

	return report



def forecastOutputMoni():
	print 'forecastOutputMoni'
	latest_foreoutput_sql = ('SELECT forecast_date, sum(count_location) as sum_states from ((SELECT forecast_date, location, count(location) as count_location FROM forecastdev.forecast_output WHERE forecast_date = (SELECT MAX(forecast_date) FROM forecastdev.forecast_output) group by location) as count_table)')
	foreoutput_data = pd.read_sql(latest_foreoutput_sql,db)

	updated_date = foreoutput_data['forecast_date'][0]
	num_states = foreoutput_data['sum_states'][0]

	### Show report
	report={}
	conclude = False
	if int(num_states) == 183060:
		conclude = True
	message = ''
	message += 'The latest update day is: '+str(updated_date)+'\n'
	message += 'There are '+ str(num_states)+ ' have been generated today!\n'

	report['updated_date']=updated_date
	report['conclude']=conclude
	report['message']=message

	return report


### forecast daily data 
def pull_forecast_daily(forecast_date, start_date, end_date):
	global server
	db = MySQLdb.connect(server_url,"observ","forecast123","forecastdev" )

	forecast_date = '"'+forecast_date+'"'
	start_date = '"'+start_date+'"'
	end_date = '"'+end_date+'"'

	query = ("SELECT date,month(date) as month, day(date) as day, sum(value) as value FROM forecastdev.forecast_daily where forecast_date="+forecast_date+" AND date>"+start_date+" AND date<"+end_date+" group by date")
	df = pd.read_sql(query, db)

	return df[['date','month','day','value']]


def pull_eia_daily(start_date, end_date):
	global server
	db = MySQLdb.connect(server_url,"observ","forecast123","forecastdev" )

	start_date = '"'+start_date+'"'
	end_date = '"'+end_date+'"'

	query = ("SELECT month(date) as month, day(date) as day, sum(value) as eia_value FROM forecastdev.eia_daily where date>"+start_date+" AND date<"+end_date+" group by date")
	df = pd.read_sql(query, db)
	return df[['month','day','eia_value']]

def foreDailyMoni():
	print 'foreDailyMoni'
	db = MySQLdb.connect(server_url,"observ","forecast123","forecastdev" )
	query = ('SELECT max(forecast_date) as date FROM forecastdev.forecast_daily;')
	updated_date = pd.read_sql(query, db)['date'][0]
	latest_date = str(updated_date)


	f_end= str(updated_date+relativedelta(days=15))
	us_15days_predict = pull_forecast_daily(latest_date,latest_date,f_end)


	e_start = str(updated_date-relativedelta(years=1))
	e_end = str(updated_date+relativedelta(days=15)-relativedelta(years=1))
	us_15days_predict = us_15days_predict.merge(pull_eia_daily(e_start,e_end),how='left', on=['month','day'])
	us_15days_predict['ratio'] = us_15days_predict['value']/us_15days_predict['eia_value']

	report = {}	
	conclude = True
	for ratio in us_15days_predict['ratio']:
		if ratio < 0.5:
			conclude = False
	message = ''
	message += 'The latest update day is: '+str(updated_date)+'\n'

	report['updated_date']=updated_date
	report['conclude']=conclude
	report['message']=message
	report['value']=us_15days_predict[['date','value']].as_matrix()
	report['eia_value']=us_15days_predict[['date','eia_value']].as_matrix()
	forecast_daily_list = []
	eia_daily_list = []
	forecast_eia = []
	for element in report['value']:
		forecast_daily_list.append([int(time.mktime(element[0].timetuple())*1000),element[1]])
	for element in report['eia_value']:
		eia_daily_list.append([int(time.mktime(element[0].timetuple())*1000),element[1]])

	forecast_eia = [forecast_daily_list, eia_daily_list]

	return forecast_eia


### forecast monthly data
def period():
	now = pd.datetime.today().date()
	now -=timedelta(days=now.day-1)
	# EIA release data 2 month ago
	old_start_date = now-relativedelta(months=12)
	old_end_date = now
	fore_start_date = now
	fore_end_date = now +relativedelta(months=12)
	return old_start_date, old_end_date, fore_start_date, fore_end_date

states = ('AL','AR','AZ','CA','CO','CT','DC','DE','FL','GA','IA',
			'ID','IL','IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT',
			'NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC',
			'SD','TN','TX','UT','VA','VT','WA','WI','WV','WY')


def get_US_forecast(fore_start_date, fore_end_date, forecast_date):
	global server_url
	fore_start_date = "'"+str(fore_start_date)+"'"
	fore_end_date = "'"+str(fore_end_date)+"'"
	forecast_date = "'"+str(forecast_date)+"'"
	db = MySQLdb.connect(server_url,"observ","forecast123","forecastdev" )
	query = ("SELECT date,year(date) as year,month(date) as month,sum(median) as median FROM forecastdev.forecast_monthly" 	
			" WHERE forecast_date = "+ forecast_date+ 'and location in '+str(states)+ " and date>"+fore_start_date+" and date<"+fore_end_date+
			" GROUP BY date")
	df = pd.read_sql(query, db)

	return df

def get_US_burn(old_start_date, old_end_date):
	global server
	old_start_date = "'"+str(old_start_date)+"'"
	old_end_date = "'"+str(old_end_date)+"'"
	db = MySQLdb.connect(server_url,"observ","forecast123","eiadev" )
	query = ("SELECT year(date) as year,month(date) as month, sum(value)/DAY(LAST_DAY(date)) as eia_value"
			" FROM"
    		" eiadev.obs_state2"
        	" JOIN"
    		" eiadev.eia_series ON obs_state2.id = eiadev.eia_series.obs_state_id"
        	" JOIN"
    		" eiadev.eia_data ON eia_data.eia_series_id = eia_series.eia_series_id"
			" WHERE"
    		" eiadev.eia_series.name LIKE '%elec%' and eiadev.obs_state2.state_code in "+str(states)+" and date<"+old_end_date+" and date>"+old_start_date+
			" group by date")
	df = pd.read_sql(query, db)

	return df

def foreMonMoni():
	print 'foreMonMoni'
	global server_url
	db = MySQLdb.connect(server_url,"observ","forecast123","forecastdev" )
	query = ('SELECT max(forecast_date) as date FROM forecastdev.forecast_monthly;')

	updated_date = pd.read_sql(query, db)['date'][0]
	forecast_date = str(updated_date)

	observserver = MySQLdb.connect(server_url,"observ","forecast123","observserver")
	old_start_date, old_end_date, fore_start_date, fore_end_date = period()
	us = get_US_forecast(fore_start_date, fore_end_date, forecast_date)
	us = us.merge(get_US_burn(old_start_date, old_end_date),how = 'left', on = ['month'])

	report={}
	conclude = True
	message=''

	us['ratio'] = us['median']/us['eia_value']
	for ratio in us['ratio']:
		if ratio<0.5:
			conclude = False
	message += 'The latest update day is: '+str(updated_date)+'\n'

	report['updated_date']=updated_date
	report['conclude']=conclude
	report['message']=message
	report['eia_value']=us[['date','eia_value']].dropna().as_matrix()
	report['median']=us[['date','median']].as_matrix()

	forecast_monthly_list = []
	eia_monthly_list = []
	forecast_monthly_eia = []

	for element in report['median']:
		forecast_monthly_list.append([int(time.mktime(element[0].timetuple())*1000),element[1]])
	for element in report['eia_value']:
		eia_monthly_list.append([int(time.mktime(element[0].timetuple())*1000),element[1]])
	
	forecast_monthly_eia = [forecast_monthly_list, eia_monthly_list]
	return forecast_monthly_eia
	
