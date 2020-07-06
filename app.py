import cx_Oracle
import pandas as pd
from pandas import DataFrame
from pandas import Series
import numpy as np
import datetime
from utils.helper import *
from reports.history import *
from reports.cathodics import *
import flask
from db.models import *
from flask import Flask
from flask import redirect

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import dateutil.relativedelta
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from dash import Dash
from flask import request
from flask import send_from_directory
from pyexcelerate import Workbook
import time
from werkzeug.serving import run_simple
import urllib.parse
import plotly.graph_objects as go

from views.cathodic_view import *


server = Flask(__name__)



start_time = time.time()

def df_to_excel(df, path, sheet_name='Sheet 1'):
    data = [df.columns.tolist(), ] + df.values.tolist()
    wb = Workbook()
    wb.new_sheet(sheet_name, data=data)
    wb.save(path)

@server.route('/')
def index():
    return 'Server Works!'
  
@server.route('/data_science/history_events')
def history_events():
    print ('hello reports')
    req = request.args.to_dict(flat=True)
    user = query_user(req)
    data_historics = query_historics(request.args.to_dict(flat=True))
    data_incidents = query_incidents(request.args.to_dict(flat=True))
    data_report = pd.concat([data_historics, data_incidents])
    data_report = data_report.sort_index()
    data_report['DATE_ENTRY']= pd.to_datetime(data_report['DATE_ENTRY']) 

    data_report.sort_values('DATE_ENTRY', inplace=True, ascending=False)
    data_report['DATE_ENTRY'] = data_report['DATE_ENTRY'].dt.tz_localize('GMT').dt.tz_convert(user.time_zone)
    column_keys = ['PLATE', 'INTERNAL_CODE', 'DATE_ENTRY','EVENT_NAME','VALUE','ADDRESS', 'X', 'Y', 'SPEED', 'ORIENTATION', 'BATTERY', 'SHEET']
    translaters = data_report['EVENT_NAME'].unique().tolist() + [x.lower() for x in column_keys]
    data_report['EVENT_NAME'] = data_report['EVENT_NAME'].apply(lambda x: translate(x, translaters, user.locale))
    
    column_names = []

    for c in column_keys:
        column_names.append(translate(c.lower(), translaters, user.locale))
    
    data_report = data_report[column_keys]
    data_report.columns = column_names
    
    owner_id = str(user.owner_id)
    full_path = os.path.dirname(os.path.abspath(__file__))

    data_report.to_csv(full_path+'/history_events'+owner_id+'.csv', index=False)

    return send_from_directory(full_path, 'history_events'+owner_id+'.csv', as_attachment=True)


@server.route('/data_science/history_cathodics_recti')
def history_cathodics_recti():
    print ('hello history_cathodics_recti')
    req = request.args.to_dict(flat=True)
    user = query_user(req)
    cathodics_recti = query_recti(req)
    data_report = pd.concat([cathodics_recti])
    data_report = data_report.sort_index()
    data_report['HICAFEEN']= pd.to_datetime(data_report['HICAFEEN']) 
    data_report.sort_values('HICAFEEN', inplace=True, ascending=False)
    column_keys = [ 'STATION_NAME','STATION_TYPE','TYPE_LINE','HICAFEEN','HICAVOSA','HICAVOSH','HICACOTU','HICAVOAC','HICACOAC','HICAESTA','HICAPDON','HICAPDOF' ]
    translaters = [x.lower() for x in column_keys]
 
    
    column_names = []

    for c in column_keys:
        column_names.append(translate(c, translaters, user.locale))
    
    data_report = data_report[column_keys]
    data_report.columns = column_names
    owner_id = str(user.owner_id)

    full_path = os.path.dirname(os.path.abspath(__file__))    
    #data_report.to_excel(full_path+'/history_cathodics_recti'+owner_id+'.xlsx', index=False)
    data_report.to_csv(full_path+'/history_cathodics_recti'+owner_id+'.csv', index=False)
    return send_from_directory(full_path, 'history_cathodics_recti'+owner_id+'.csv', as_attachment=True)

@server.route('/data_science/history_cathodics_thermo')
def history_cathodics_thermo():
    print ('hello history_cathodics_thermo')
    total_time = time.time()
    req = request.args.to_dict(flat=True)
    user = query_user(req)
    cathodics_thermo = query_thermo(req)
    data_report = pd.concat([cathodics_thermo])
    data_report = data_report.sort_index()
    data_report['HICAFEEN']= pd.to_datetime(data_report['HICAFEEN']) 
    data_report.sort_values('HICAFEEN', inplace=True, ascending=False)
    column_keys = [ 'STATION_NAME','STATION_TYPE','TYPE_LINE','HICAFEEN','HICAVOSA','HICAVOSH','HICACOTU','HICAVOAC','HICACOAC','HICAESTA','HICAPDON','HICAPDOF' ]
    translaters = [x.lower() for x in column_keys]

    
    column_names = []

    for c in column_keys:
        column_names.append(translate(c, translaters, user.locale))
    
    data_report = data_report[column_keys]
    data_report.columns = column_names
    owner_id = str(user.owner_id)
    start_time = time.time()
    print("--- %s creating file' ---" % (time.time() - start_time))
    full_path = os.path.dirname(os.path.abspath(__file__))    

    #data_report.to_excel(full_path+'/history_cathodics_thermo'+owner_id+'.xlsx', index=False)
    #print("--- %s creating file xlsx1' ---" % (time.time() - start_time))
    start_time = time.time()
    data_report.to_csv(full_path+'/history_cathodics_thermo'+owner_id+'.csv', index=False)
    print("--- %s creating file csv' ---" % (time.time() - start_time))
    #start_time = time.time()
   # df_to_excel(data_report,full_path+'/history_cathodics_thermo'+owner_id+'.xlsx',sheet_name='history_cathodics_thermo')
    #print("--- %s creating file xlsx2' ---" % (time.time() - start_time))
    #start_time = time.time()

    print("--- %s total time' ---" % (time.time() - total_time))


    return send_from_directory(full_path, 'history_cathodics_thermo'+owner_id+'.csv', as_attachment=True)



    


@server.route('/data_science/history_cathodics_daily')
def history_cathodics_daily():
    print ('hello history_cathodics_daily')
    req = request.args.to_dict(flat=True)
    user = query_user(req)
    cathodics_daily = query_daily(req)
    data_report = pd.concat([cathodics_daily])
    data_report = data_report.sort_index()
    data_report['HICAFEEN']= pd.to_datetime(data_report['HICAFEEN']) 
    data_report.sort_values('HICAFEEN', inplace=True, ascending=False)
    column_keys = [ 'STATION_NAME','STATION_TYPE','TYPE_LINE','HICAFEEN','HICAVOSA','HICAVOSH','HICACOTU','HICAVOAC','HICACOAC','HICAESTA' ]
    translaters = [x.lower() for x in column_keys]


    
    column_names = []

    for c in column_keys:
        column_names.append(translate(c, translaters, user.locale))

    data_report = data_report[column_keys]
    data_report.columns = column_names
    owner_id = str(user.owner_id)
    
    full_path = os.path.dirname(os.path.abspath(__file__))
    #data_report.to_excel(full_path+'/history_cathodics_daily'+owner_id+'.xlsx', index=False)
    data_report.to_csv(full_path+'/history_cathodics_daily'+owner_id+'.csv', index=False)
    return send_from_directory(full_path, 'history_cathodics_daily'+owner_id+'.csv', as_attachment=True)




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_thermo = Dash(__name__, server = server, url_base_pathname='/data_science/thermo/',  external_stylesheets=external_stylesheets )
dash_recti = Dash(__name__, server = server, url_base_pathname='/data_science/recti/',  external_stylesheets=external_stylesheets )
dash_thermo.layout = custom_layout()
dash_recti.layout = custom_layout()


@dash_recti.callback(
    Output("stations", "options"),
    [Input("stations", "search_value")],
)
def update_dropdown_stations(wdg):
    print('update_dropdown_stations')
    parsed_query = urllib.parse.urlparse( flask.request.headers.get('Referer') )
    pur = parse_url_params( parsed_query )
    mobiles =  [{'label':i['plate'],'value':(i['id'])} for i in filter(driver_filter, query_mobiles(pur))] 
    return mobiles

def driver_filter(mobile):
    parsed_query = flask.request.headers.get('Referer') 
    mode = ''
    if 'thermo' in parsed_query:
        mode = 'TERMOGENERADOR'
    if 'recti' in parsed_query:
        mode = 'RECTIFICADOR'
    print(mode)
    return mobile['driver'] == mode

@dash_thermo.callback(
    Output("stations", "options"),
    [Input("stations", "search_value")],
)
def update_dropdown_stations(wdg):
    print('update_dropdown_stations')
    parsed_query = urllib.parse.urlparse( flask.request.headers.get('Referer') )
    pur = parse_url_params( parsed_query )
    mobiles =  [{'label':i['plate'],'value':(i['id'])} for i in filter(driver_filter, query_mobiles(pur))] 
    return mobiles


@dash_thermo.callback(
   [ Output('datatable-timeframed', 'data'),
     Output('datatable-timeframed', 'columns'),
      Output('link-csv', 'href')],
    [   Input('datatable-timeframed', "page_current"), 
        Input('datatable-timeframed', "page_size"), 
        Input('url', "pathname"),
        Input('report-date', 'start_date'),
        Input('report-date', 'end_date'),
        Input('timeframes', 'value'),
        Input('button', 'n_clicks'),
        Input('stations', 'value')
    ]
    )
def update_table_framed(page_current,page_size, url, start_date, end_date, timeframe, n_clicks, stations):
    return mupdate_table_framed(page_current,page_size, url, start_date, end_date, timeframe, n_clicks, stations, flask.request.headers.get('Referer') )


@dash_recti.callback(
   [ Output('datatable-timeframed', 'data'),
     Output('datatable-timeframed', 'columns'),
     Output('link-csv', 'href')],
    [   Input('datatable-timeframed', "page_current"), 
        Input('datatable-timeframed', "page_size"), 
        Input('url', "pathname"),
        Input('report-date', 'start_date'),
        Input('report-date', 'end_date'),
        Input('timeframes', 'value'),
        Input('button', 'n_clicks'),
        Input('stations', 'value')
    ]
)
def update_table_framed(page_current,page_size, url, start_date, end_date, timeframe, n_clicks, stations):
    return mupdate_table_framed(page_current,page_size, url, start_date, end_date, timeframe, n_clicks, stations, flask.request.headers.get('Referer') )

@server.route('/data_science/thermo/file.csv')
def thermo_csv():
    parsed_query = urllib.parse.urlparse( flask.request.headers.get('Referer') )
    pur = parse_url_params( parsed_query )
    user = query_user(pur)
    full_path = os.path.dirname(os.path.abspath(__file__)) + '/views/'

    owner_id = str(user.owner_id)
    return send_from_directory(full_path, 'cathodics_data'+owner_id+'.csv', as_attachment=True)

@server.route('/data_science/recti/file.csv')
def recti_csv():
    parsed_query = urllib.parse.urlparse( flask.request.headers.get('Referer') )
    pur = parse_url_params( parsed_query )
    user = query_user(pur)
    full_path = os.path.dirname(os.path.abspath(__file__)) + '/views/'
    owner_id = str(user.owner_id)
    return send_from_directory(full_path, 'cathodics_data'+owner_id+'.csv', as_attachment=True)

if (__name__ == '__main__'):
    server.run(host='0.0.0.0')

