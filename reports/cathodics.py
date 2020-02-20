import os
import cx_Oracle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from db.models import *
from utils.helper import *


def query_thermo(request):
    
   # plates =  request.get('plates').replace('[','').replace(']','').replace('"', '\'')  
    user = query_user(request)
    idStation = request.get('idStation')
    print(idStation)
    mobile_ids = []
    if str(idStation)=='0':
        print('idStation')
        print(idStation)
        plate = OwnerPlate.objects.filter(owner_id = user.owner_id).values_list('plate', flat=True)
        mobile_ids = Mobile.objects.filter(plate__in = plate).values_list('id', flat=True)
        mobile_ids = str(list(mobile_ids)).replace("[","").replace("]","")
    else:
        plate = OwnerPlate.objects.filter(id = idStation).values_list('plate', flat=True)
        mobile_ids = Mobile.objects.filter(plate__in = plate).values_list('id', flat=True)
        mobile_ids = str(list(mobile_ids)).replace("[","").replace("]","")


    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech")
    sql = ' SELECT cathodic_historics.plate as station_name, driver as station_type, type_line, "CATHODIC_HISTORICS"."HICAFEEN", "CATHODIC_HISTORICS"."HICAVOSA", "CATHODIC_HISTORICS"."HICAVOSH", "CATHODIC_HISTORICS"."HICACOTU", "CATHODIC_HISTORICS"."HICAVOAC", "CATHODIC_HISTORICS"."HICACOAC", "CATHODIC_HISTORICS"."HICAESTA", cathodic_levels.canipome, cathodic_levels.canipoba, cathodic_levels.canivotu, cathodic_levels.canicotu, cathodic_levels.canivosh FROM "CATHODIC_HISTORICS" INNER JOIN OWNER_PLATES ON OWNER_PLATES.plate = CATHODIC_HISTORICS.plate INNER JOIN CATHODIC_LEVELS ON CATHODIC_LEVELS.MOBILE_ID = CATHODIC_HISTORICS.MOBILE_ID WHERE CATHODIC_HISTORICS.mobile_id in ('+(mobile_ids)+') and "OWNER_PLATES"."OWNER_ID" = :owner_id AND (hicafeen between to_date(:fecha_inicial_reporte,\'dd/mm/yyyy hh24:mi:ss\') and to_date(:fecha_final_reporte,\'dd/mm/yyyy hh24:mi:ss\')) AND "OWNER_PLATES"."DRIVER" = :driver ORDER BY owner_plates.plate asc, CATHODIC_HISTORICS.HICAFEEN desc '
    print(sql)
    curs = conn.cursor()
    curs.prepare(sql)

   
    owner_id = user.owner_id
    #print(owner_id)
    curs.execute(None, 
                 {'owner_id': owner_id,  
                 'driver': 'TERMOGENERADOR',  
                  'fecha_inicial_reporte': request.get('fecha_inicial_reporte') ,  
                  'fecha_final_reporte': request.get('fecha_final_reporte')   
                
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
    
def query_recti(request):
    
   # plates =  request.get('plates').replace('[','').replace(']','').replace('"', '\'')  
    user = query_user(request)
    idStation = request.get('idStation')
    print(idStation)
    mobile_ids = []
    if str(idStation)=='0':
        print('idStation')
        print(idStation)
        plate = OwnerPlate.objects.filter(owner_id = user.owner_id).values_list('plate', flat=True)
        mobile_ids = Mobile.objects.filter(plate__in = plate).values_list('id', flat=True)
        mobile_ids = str(list(mobile_ids)).replace("[","").replace("]","")
    else:
        plate = OwnerPlate.objects.filter(id = idStation).values_list('plate', flat=True)
        mobile_ids = Mobile.objects.filter(plate__in = plate).values_list('id', flat=True)
        mobile_ids = str(list(mobile_ids)).replace("[","").replace("]","")


    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech")
    sql = ' SELECT cathodic_historics.plate as station_name, driver as station_type, type_line, "CATHODIC_HISTORICS"."HICAFEEN", "CATHODIC_HISTORICS"."HICAVOSA", "CATHODIC_HISTORICS"."HICAVOSH", "CATHODIC_HISTORICS"."HICACOTU", "CATHODIC_HISTORICS"."HICAVOAC", "CATHODIC_HISTORICS"."HICACOAC", "CATHODIC_HISTORICS"."HICAESTA", cathodic_levels.canipome, cathodic_levels.canipoba, cathodic_levels.canivotu, cathodic_levels.canicotu, cathodic_levels.canivosh FROM "CATHODIC_HISTORICS" INNER JOIN OWNER_PLATES ON OWNER_PLATES.plate = CATHODIC_HISTORICS.plate INNER JOIN CATHODIC_LEVELS ON CATHODIC_LEVELS.MOBILE_ID = CATHODIC_HISTORICS.MOBILE_ID WHERE CATHODIC_HISTORICS.mobile_id in ('+(mobile_ids)+') and "OWNER_PLATES"."OWNER_ID" = :owner_id AND (hicafeen between to_date(:fecha_inicial_reporte,\'dd/mm/yyyy hh24:mi:ss\') and to_date(:fecha_final_reporte,\'dd/mm/yyyy hh24:mi:ss\')) AND "OWNER_PLATES"."DRIVER" = :driver ORDER BY owner_plates.plate asc, CATHODIC_HISTORICS.HICAFEEN desc '
    print(sql)
    curs = conn.cursor()
    curs.prepare(sql)

   
    owner_id = user.owner_id
    #print(owner_id)
    curs.execute(None, 
                 {'owner_id': owner_id,  
                 'driver': 'RECTIFICADOR',  
                  'fecha_inicial_reporte': request.get('fecha_inicial_reporte') ,  
                  'fecha_final_reporte': request.get('fecha_final_reporte')   
                
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

def query_max_daily(request):
    print (query_max_daily)
    user = query_user(request)
    idStation = request.get('idStation')
    print(idStation)
    mobile_ids = []
    if str(idStation)=='0':
        print('idStation')
        print(idStation)
        plate = OwnerPlate.objects.filter(owner_id = user.owner_id).values_list('plate', flat=True)
        mobile_ids = Mobile.objects.filter(plate__in = plate).values_list('id', flat=True)
        mobile_ids = str(list(mobile_ids)).replace("[","").replace("]","")
    else:
        plate = OwnerPlate.objects.filter(id = idStation).values_list('plate', flat=True)
        mobile_ids = Mobile.objects.filter(plate__in = plate).values_list('id', flat=True)
        mobile_ids = str(list(mobile_ids)).replace("[","").replace("]","")


    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech")
    sql = ' SELECT max("CATHODIC_HISTORICS".id) as id, "CATHODIC_HISTORICS".plate FROM "CATHODIC_HISTORICS" INNER JOIN OWNER_PLATES ON OWNER_PLATES.plate = "CATHODIC_HISTORICS".plate INNER JOIN CATHODIC_LEVELS ON CATHODIC_LEVELS.MOBILE_ID = "CATHODIC_HISTORICS".MOBILE_ID WHERE "CATHODIC_HISTORICS".mobile_id in ('+(mobile_ids)+') and "OWNER_PLATES"."OWNER_ID" = :owner_id AND (hicafeen between to_date(:fecha_inicial_reporte,\'dd/mm/yyyy hh24:mi:ss\') and to_date(:fecha_final_reporte,\'dd/mm/yyyy hh24:mi:ss\')) AND "OWNER_PLATES"."DRIVER" in (\'TERMOGENERADOR\', \'RECTIFICADOR\') GROUP BY "CATHODIC_HISTORICS".PLATE  '

    owner_id = user.owner_id
    curs = conn.cursor()
    curs.prepare(sql)
    curs.execute(None, 
                 {'owner_id': owner_id,   
                  'fecha_inicial_reporte': request.get('fecha_inicial_reporte') ,  
                  'fecha_final_reporte': request.get('fecha_final_reporte')                   
                 }
                 
                
                )
    df2 = DataFrame(curs.fetchall())
    data_max_daily = df2
    c = 0
    column_names = []
    for column in curs.description:
        column_names.append(curs.description[c][0])
        c += 1

    try:
        data_max_daily.columns = column_names
    except:
        data_max_daily.columns = data_max_daily.columns
    conn.close()
    print (data_max_daily.ID.values)
    return data_max_daily.ID

def query_daily(request):
    
   # plates =  request.get('plates').replace('[','').replace(']','').replace('"', '\'')  
    user = query_user(request)
    idStation = request.get('idStation')
    print(idStation)
    mobile_ids = []
    if str(idStation)=='0':
        print('idStation')
        print(idStation)
        plate = OwnerPlate.objects.filter(owner_id = user.owner_id).values_list('plate', flat=True)
        mobile_ids = Mobile.objects.filter(plate__in = plate).values_list('id', flat=True)
        mobile_ids = str(list(mobile_ids)).replace("[","").replace("]","")
    else:
        plate = OwnerPlate.objects.filter(id = idStation).values_list('plate', flat=True)
        mobile_ids = Mobile.objects.filter(plate__in = plate).values_list('id', flat=True)
        mobile_ids = str(list(mobile_ids)).replace("[","").replace("]","")

    ids = str(list(query_max_daily(request))).replace("[","").replace("]","")
    print(ids)

    sql = ' SELECT cathodic_historics.plate as station_name, driver as station_type, type_line, "CATHODIC_HISTORICS"."HICAFEEN", "CATHODIC_HISTORICS"."HICAVOSA", "CATHODIC_HISTORICS"."HICAVOSH", "CATHODIC_HISTORICS"."HICACOTU", "CATHODIC_HISTORICS"."HICAVOAC", "CATHODIC_HISTORICS"."HICACOAC", "CATHODIC_HISTORICS"."HICAESTA", cathodic_levels.canipome, cathodic_levels.canipoba, cathodic_levels.canivotu, cathodic_levels.canicotu, cathodic_levels.canivosh FROM "CATHODIC_HISTORICS" INNER JOIN OWNER_PLATES ON OWNER_PLATES.plate = CATHODIC_HISTORICS.plate INNER JOIN CATHODIC_LEVELS ON CATHODIC_LEVELS.MOBILE_ID = CATHODIC_HISTORICS.MOBILE_ID WHERE CATHODIC_HISTORICS.id in ('+ids+') and "OWNER_PLATES"."OWNER_ID" = :owner_id ORDER BY owner_plates.plate asc, CATHODIC_HISTORICS.HICAFEEN desc '
    print(sql)
    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech")
    curs = conn.cursor()
    curs.prepare(sql)

   
    owner_id = user.owner_id
    #print(owner_id)
    curs.execute(None, 
                 {'owner_id': owner_id              
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

    