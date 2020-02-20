import os
import cx_Oracle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from db.models import *
from utils.helper import *


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