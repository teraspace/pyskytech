import cx_Oracle
import pandas as pd
from pandas import DataFrame
from pandas import Series
import numpy as np
import datetime
from utils.helper import *
from reports.history import *
from reports.cathodics import *

from db.models import *
from flask import Flask
app = Flask(__name__)
from flask import request
from flask import send_from_directory


@app.route('/')
def index():
    return 'Server Works!'
  
@app.route('/data_science/history_events')
def history_events():
    print ('hello reports')
    req = request.args.to_dict(flat=True)
    user = query_user(req)
    data_historics = query_historics(request.args.to_dict(flat=True))
    data_incidents = query_incidents(request.args.to_dict(flat=True))
    data_report = pd.concat([data_historics, data_incidents])
    data_report = data_report.sort_index()
    data_report.sort_values('DATE_ENTRY', inplace=True, ascending=False)
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




@app.route('/data_science/history_cathodics_thermo')
def history_cathodics_thermo():
    print ('hello history_cathodics_thermo')
    req = request.args.to_dict(flat=True)
    user = query_user(req)
    cathodics_thermo = query_thermo(req)
    data_report = pd.concat([cathodics_thermo])
    data_report = data_report.sort_index()
    data_report.sort_values('HICAFEEN', inplace=True, ascending=False)
    column_keys = [ 'STATION_NAME','STATION_TYPE','TYPE_LINE','HICAFEEN','HICAVOSA','HICAVOSH','HICACOTU','HICAVOAC','HICACOAC','HICAESTA' ]
    translaters = [x.lower() for x in column_keys]

    
    column_names = []

    for c in column_keys:
        column_names.append(translate(c, translaters, user.locale))
    
    data_report = data_report[column_keys]
    data_report.columns = column_names
    owner_id = str(user.owner_id)

    
    data_report.to_csv(full_path+'/history_cathodics_thermo'+owner_id+'.csv', index=False)

    return send_from_directory(full_path, 'history_cathodics_thermo'+owner_id+'.csv', as_attachment=True)



@app.route('/data_science/history_cathodics_daily')
def history_cathodics_daily():
    print ('hello history_cathodics_daily')
    req = request.args.to_dict(flat=True)
    user = query_user(req)
    cathodics_daily = query_daily(req)
    data_report = pd.concat([cathodics_daily])
    data_report = data_report.sort_index()
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
    data_report.to_csv(full_path+'/history_cathodics_daily'+owner_id+'.csv', index=False)

    return send_from_directory(full_path, 'history_cathodics_daily'+owner_id+'.csv', as_attachment=True)

        


    

if (__name__ == '__main__'):
    app.run(host='0.0.0.0')

