
# coding: utf-8

# In[1]:


def fields(cursor):
    """ Given a DB API 2.0 cursor object that has been executed, returns
    a dictionary that maps each field name to a column index; 0 and up. """
    results = []
    column = 0
    for d in cursor.description:
        results.insert(column, d[0])
        column = column + 1

    return results


# In[2]:


# to parse the timestamps for this person
def process_datetime(dt):
    '''a simple function to parse string time into several components'''
    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    return [dt.weekday(), dt.hour]  # you can modify here to get other time components


# In[3]:


import cx_Oracle
import pandas as pd
from pandas import DataFrame

from pandas import Series
import numpy as np

import datetime

#import plotly
#plotly.tools.set_credentials_file(username='carlosman79', api_key='hr7364U5bGLVEEsqNZmr')
#import plotly.plotly as py
#import plotly.graph_objs as go


cx_Oracle.clientversion()
df_translations = []


# In[4]:


def query_translator(locale):
    print('query_translator')
    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech", encoding='UTF-8', nencoding='UTF-8')
    sql = "SELECT * from translations where locale = :locale"
    curs = conn.cursor()
    curs.prepare(sql)
    curs.execute(None, {'locale': locale})
    df_translator = DataFrame(curs.fetchall())
    
    c = 0
    column_names = []
    for column in curs.description:
        column_names.append(curs.description[c][0])
        c += 1

    df_translator.columns = column_names

    conn.close()
    return df_translator
    #df_translator = pd.read_sql(sql, conn, parse_dates=True)


# In[5]:


def query_translator_words(locale,words):
    print('query_translator_words')
    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech", encoding='UTF-8', nencoding='UTF-8')
    words =  str(words).replace('[','').replace(']','').replace('"', '\'')  
    sql = "SELECT distinct key, value from translations where locale = :locale and key in (" + words + ")"

    curs = conn.cursor()
    curs.prepare(sql)
    curs.execute(None, {'locale': locale})
    df_translator = DataFrame(curs.fetchall())
    
    c = 0
    column_names = []
    for column in curs.description:
        column_names.append(curs.description[c][0])
        c += 1
    df_translator.columns = column_names

    conn.close()
    return df_translator


# In[6]:


def translate(key, words):
    global df_translations
    if ( not isinstance( df_translations, (DataFrame)  ) ):
        if (words==None):
            df_translations = query_translator('es')
        else:
            df_translations = query_translator_words('es', words)
        #print(type(df_translations))
    #filter = df_translations["KEY"]==key

    df_found = df_translations[df_translations.KEY == key.lower()]
    try:
        return df_found.VALUE.item()
    except:
        return key


# In[7]:


'soat'.lower()


# In[13]:


def query_incidents(args):
    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech", encoding='UTF-8', nencoding='UTF-8')
    plates =  args.get('plates').replace('[','').replace(']','').replace('"', '\'')  
    
    
    events = []
    for e in args.get('events_ids').replace('[','').replace(']','').replace('"', '\'').split(','):
            events.append(str(e))

            
    events =  str(args.get('events_ids')).replace('[','').replace(']','').replace('"', '\'')

    sql = "SELECT /*+ index(INCIDENTS,INCIDENTS_INDEX3CDESC) */ incidents.ID, incidents.PLATE, incidents.ADDRESS,X, Y, DATE_ENTRY as date_entry_date , DATE_SYSTEM AS date_system_date,to_char( DATE_ENTRY, 'dd/mm/yyyy hh24:mi:ss' ) as DATE_ENTRY , to_char( DATE_SYSTEM, 'dd/mm/yyyy hh24:mi:ss' ) as DATE_SYSTEM ,to_timestamp( to_char(DATE_ENTRY, 'dd/mm/yyyy hh24:mi:ss'), 'dd/mm/yyyy hh24:mi:ss' ) as date_time_entry ,ORIENTATION,SPEED,incidents.MOBILE_ID,incidents.EVENT_ID, incidents.VALUE,incidents.description as DESCRIPTION_EVENT, incidents.description as event_name,BATTERY,SHEET,null as camera  ,incidents.INTERNAL_CODE  FROM incidents left join  \"OWNER_PLATES\" pl ON pl.plate=incidents.plate and pl.owner_id = :owner_id left join  \"OWNER_EVENTS\" ev ON ev.event_id=incidents.event_id and ev.owner_id = :owner_id left join  \"OWNER_DRIVERS\" dri ON dri.id=pl.OWNER_DRIVER_ID  WHERE  date_entry between       to_date(:fecha_inicial, 'dd/mm/yyyy hh24:mi:ss') and     to_date(:fecha_final, 'dd/mm/yyyy hh24:mi:ss') and ev.PAGE = 1  AND   incidents.plate in(" + plates + ")  and incidents.event_id in(" + events + ")  ORDER BY incidents.plate ASC, date_entry desc"
    
    curs = conn.cursor()
    curs.prepare(sql)

    curs.execute(None, 
                 {'owner_id': args.get('owner_id'),  
                  'fecha_inicial': args.get('fecha_inicial') ,  
                  'fecha_final': args.get('fecha_final')
                 
                 }
                 
                
                )
    df2 = DataFrame(curs.fetchall())
    data_incidents = df2
    c = 0
    column_names = []
    for column in curs.description:
        column_names.append(curs.description[c][0])
        c += 1
    try:
        data_incidents.columns = column_names
    except:
        data_incidents.columns = data_incidents.columns

    conn.close()
    return data_incidents


# In[14]:


def query_historics(args):
    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech", encoding='UTF-8', nencoding='UTF-8')
    plates =  args.get('plates').replace('[','').replace(']','').replace('"', '\'')  
    
    
    events = []
    for e in args.get('events_ids').replace('[','').replace(']','').replace('"', '\'').split(','):
            events.append(str(e))

            
    events =  str(args.get('events_ids')).replace('[','').replace(']','').replace('"', '\'')

    sql = "SELECT /*+ index(historics,HISTORICS_INDEX3CDESC) */ historics.ID, historics.PLATE, historics.ADDRESS,X, Y, DATE_ENTRY as date_entry_date , DATE_SYSTEM AS date_system_date,to_char( DATE_ENTRY, 'dd/mm/yyyy hh24:mi:ss' ) as DATE_ENTRY , to_char( DATE_SYSTEM, 'dd/mm/yyyy hh24:mi:ss' ) as DATE_SYSTEM ,to_timestamp( to_char(DATE_ENTRY, 'dd/mm/yyyy hh24:mi:ss'), 'dd/mm/yyyy hh24:mi:ss' ) as date_time_entry ,ORIENTATION,SPEED,historics.MOBILE_ID,historics.EVENT_ID,'' as VALUE,'posicion_gps' as DESCRIPTION_EVENT,'posicion_gps' as event_name,BATTERY,SHEET,null as camera  ,historics.INTERNAL_CODE  FROM \"HISTORICS\" left join  \"OWNER_PLATES\" pl ON pl.plate=\"HISTORICS\".plate and pl.owner_id = :owner_id left join  \"OWNER_EVENTS\" ev ON ev.event_id=\"HISTORICS\".event_id and ev.owner_id = :owner_id left join  \"OWNER_DRIVERS\" dri ON dri.id=pl.OWNER_DRIVER_ID  WHERE  date_entry between       to_date(:fecha_inicial, 'dd/mm/yyyy hh24:mi:ss') and     to_date(:fecha_final, 'dd/mm/yyyy hh24:mi:ss') and ev.PAGE = 1  AND   \"HISTORICS\".plate in(" + plates + ")  and \"HISTORICS\".event_id in(" + events + ")  ORDER BY \"HISTORICS\".plate ASC, date_entry desc"

    curs = conn.cursor()
    curs.prepare(sql)

    curs.execute(None, 
                 {'owner_id': args.get('owner_id'),  
                  'fecha_inicial': args.get('fecha_inicial') ,  
                  'fecha_final': args.get('fecha_final')
                 
                 }
                 
                
                )
    df2 = DataFrame(curs.fetchall())
    data_historics = df2
    c = 0
    column_names = []
    for column in curs.description:
        column_names.append(curs.description[c][0])
        c += 1

    try:
        data_historics.columns = column_names
    except:
        data_historics.columns = data_historics.columns
    conn.close()
    return data_historics


# In[15]:


#df_all_rows.to_csv(r'/home/geotech-user/first.csv')


# In[16]:


# df_all_rows.to_excel('test.xlsx', sheet_name='sheet1', index=False)


# In[17]:


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

    
    data_historics = query_historics(request.args.to_dict(flat=True))
    data_incidents = query_incidents(request.args.to_dict(flat=True))
    data_report = pd.concat([data_historics, data_incidents])
    data_report = data_report.sort_index()
    data_report.sort_values('DATE_ENTRY', inplace=True, ascending=False)
    column_keys = ['PLATE', 'INTERNAL_CODE', 'DATE_ENTRY','EVENT_NAME','VALUE','ADDRESS', 'X', 'Y', 'SPEED', 'ORIENTATION', 'BATTERY', 'SHEET']
    translaters = data_report['EVENT_NAME'].unique().tolist() + [x.lower() for x in column_keys]
    print (translaters)
    data_report['EVENT_NAME'] = data_report['EVENT_NAME'].apply(lambda x: translate(x, translaters))
    #data_incidents['EVENT_NAME'] = data_incidents['EVENT_NAME'].apply(lambda x: translate(x))
    
    column_names = []

    for c in column_keys:
        print (translate(c, translaters))
        column_names.append(translate(c.lower(), translaters))
    
    print(column_names)
    data_report = data_report[column_keys]
    data_report.columns = column_names
    #data_incidents = data_historics[column_keys]
    #data_incidents.columns = column_names
    owner_id = request.args.to_dict(flat=True).get('owner_id')
    
        
    data_report.to_csv(r'/home/geotech-user/skytech_core/pyskytech/history_events'+owner_id+'.csv', index=False)

    return send_from_directory('/home/geotech-user/skytech_core/pyskytech',
                               'history_events'+owner_id+'.csv', as_attachment=True)
if (__name__ == '__main__'):
    app.run(host='0.0.0.0')

