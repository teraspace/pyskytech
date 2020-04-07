import cx_Oracle
import pandas as pd
from pandas import DataFrame
from reports.history import *
import urllib.parse
import requests


def parse_url_params(ref):
    parsed = {}
    print('parse_url_params')
    only_params = urllib.parse.unquote(ref.query)
    array_params = only_params.split('&')
    for item in array_params:
        parsed[item.split('=')[0]] = item.split('=')[1]
    return parsed


def get_params(flask):
    parsed_query = urllib.parse.urlparse(flask.request.headers.get('Referer') )
    pur = parse_url_params( parsed_query )
    return pur


def query_mobiles(request):
    print('query_mobiles')
    mobiles = None
    access_token = request.get('access_token')
    response = requests.get('https://api.geotechsa.co/owner_plates?access_token=' + access_token)
    
    if response.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(response.status_code))

    return response.json()['data']
def query_user(request):
    access_token = request.get('access_token')
    oat = OauthAccessToken.objects.get(token=access_token)
    user = User.objects.get(id=oat.resource_owner_id)
    if user.user_profile_id == 3:
        try:
            us = UserSupport.objects.get(token=oat.token)
            user.owner_id = us.owner_id
        except:
            print('no modificar')
    return user

def query_translator(locale):
    print('query_translator')
    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech", encoding='UTF-8', nencoding='UTF-8', threaded=True)
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


df_translations = []


def query_translator_words(locale,words):
    print('query_translator_words')
    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech", encoding='UTF-8', nencoding='UTF-8', threaded=True)
    words =  str(words).replace('[','').replace(']','').replace('"', '\'')  
    sql = "SELECT  key, value from translations where locale = :locale and key in (" + words + ")"

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



def translate(key, words, locale):
    global df_translations
    if ( not isinstance( df_translations, (DataFrame)  ) ):
        if (words==None):
            df_translations = query_translator(locale)
        else:
            df_translations = query_translator_words(locale, words)
        #print(type(df_translations))
    #filter = df_translations["KEY"]==key

    df_found = df_translations[df_translations.KEY == key.lower()]
    try:
        return df_found.VALUE.item()
    except:
        return key


def fields(cursor):
    """ Given a DB API 2.0 cursor object that has been executed, returns
    a dictionary that maps each field name to a column index; 0 and up. """
    results = []
    column = 0
    for d in cursor.description:
        results.insert(column, d[0])
        column = column + 1

    return results


# to parse the timestamps for this person
def process_datetime(dt):
    '''a simple function to parse string time into several components'''
    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    return [dt.weekday(), dt.hour]  # you can modify here to get other time components

