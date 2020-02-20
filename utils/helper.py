import cx_Oracle
import pandas as pd
from pandas import DataFrame
from reports.history import *

def query_user(request):
    access_token = request.get('access_token')
    #Room.objects.select_related('house').filter(house__street=xyz)
    oat = OauthAccessToken.objects.get(token=access_token)
    print(oat.resource_owner_id)
    user = User.objects.get(id=oat.resource_owner_id)
 
    return user

def query_translator(locale):
    print('query_translator')
    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech", encoding='UTF-8', nencoding='UTF-8')
    sql = "SELECT * from translations where locale = :locale"
    curs = conn.cursor()
    curs.prepare(sql)

    print (locale)
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
    conn = cx_Oracle.connect("skytech", "skytech", "oracle.geotech.com.co/geotech", encoding='UTF-8', nencoding='UTF-8')
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


# In[2]:


# to parse the timestamps for this person
def process_datetime(dt):
    '''a simple function to parse string time into several components'''
    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    return [dt.weekday(), dt.hour]  # you can modify here to get other time components

