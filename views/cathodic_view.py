import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import datetime
from datetime import datetime as dt
import dateutil.relativedelta
from utils.helper import *
from reports.cathodics import *
import time

start_time = time.time()
PAGE_SIZE = 30
colors = {
    'background': '#fff',
    'text': '#7FDBFF'
}

def custom_layout():
    
   return html.Div(style={'backgroundColor': colors['background']}, children=[  
    dcc.Location(id='url'),
    html.Script('document.getElementById("uuu").innerHTML = "Hello"', type="text/JavaScript"),

    html.Div(style={'backgroundColor': colors['background'], 'display':'inline'}, children=[
        dcc.DatePickerRange(
            id='report-date',
            start_date=(datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)),
            min_date_allowed=dt(datetime.datetime.now().year, 1, 1),
            max_date_allowed=dt.today(),
            initial_visible_month=(datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)),
            end_date=dt.today(),
            display_format = 'DD/MM/YYYY'
        ) ,
         html.Button('Consultar', id='button'),
    ]),
     html.Div(id='output-report-date'),
    dcc.Dropdown(
        id='stations',
        multi=True,
        clearable=False
    ) ,
        dcc.Dropdown(
        id='timeframes',
        options=[
            {'label': '1 Minutos', 'value': '1Min'},
            {'label': '5 Minutos', 'value': '5Min'},
            {'label': '15 Minutos', 'value': '15Min'},
            {'label': '30 Minutos', 'value': '30Min'},
            {'label': '1 Hora', 'value': '1H'},
            {'label': '4 Horas', 'value': '4H'},
            {'label': '1 Día', 'value': '1D'},
        ],
        value='5Min',
        multi=False,
        clearable=False
    ) ,
    # dash_table.DataTable(
    #     id='datatable-full',
    #     columns=[
    #         {"name": i, "id": i} for i in (['Estación','Tipo','Servicio','Fecha','Voltaje Salida Tubo(V)','Voltaje SHUNT(mV)','Corriente Tubo(A)','Voltaje AC(V)','Corriente AC(A)','Estado'])
    #     ],
    #     page_current=0,
    #     page_size=PAGE_SIZE,
    #     page_action='custom'
    # ),
    dcc.Loading(
            id="loading-2",
            children=[    
                    dash_table.DataTable(
                    id='datatable-timeframed',
                    page_current=0,
                    page_size=PAGE_SIZE,
                    page_action='custom'
                ),
                    html.A('Descargar CSV', id='link-csv')
                ],
                    type="circle",
                )
,
        html.Div(id='table-store', style={'display': 'none'})

])
df_cathodics = pd.DataFrame()
data_graph = pd.DataFrame()
df_full_cathodics = pd.DataFrame()

last_click = 0
last_url = ''
def mupdate_table_framed(page_current,page_size, url, start_date, end_date, timeframe, n_clicks, stations, params):

    print ('_update_table_framed')

    global last_click
    data_frame = pd.DataFrame()

    if stations==None:
        stations=''
    parsed_query = urllib.parse.urlparse(params)
  
    pur = parse_url_params( parsed_query )
    access_token = pur.get('access_token')
    # 2020-04-01T18:22:10.205774
    source_format = '%Y-%m-%d'
    target_format = '%d/%m/%Y'
    fecha_inicial_reporte = dt.strptime(start_date.split('T')[0], source_format)
    fecha_final_reporte =  dt.strptime(end_date.split('T')[0], source_format)
    query = { 'access_token': access_token,
              'fecha_inicial_reporte':   dt.strftime(fecha_inicial_reporte, target_format) + ' 00:00:00',
              'fecha_final_reporte':   dt.strftime(fecha_final_reporte, target_format) + ' 23:59:59',
              'idStation': str(stations).replace('[','').replace(']','')
            }

    global data_graph
    global df_cathodics
    global df_full_cathodics
    global last_url
    if last_url != params:
        df_cathodics = pd.DataFrame()
        data_graph = pd.DataFrame()
        df_full_cathodics = pd.DataFrame()
        last_click = 0
        last_url = params
    if n_clicks!=None:
        if last_click != n_clicks:
            df_full_cathodics = history_cathodics_data(query, params)
            last_click = n_clicks
    
    
   
    if df_full_cathodics.empty:
        print('NO HAY DATOS PARA MOSTRAR')
        return pd.DataFrame().to_dict('records')
    else:
        df_cathodics = df_full_cathodics

    data_frame = df_cathodics.set_index('Fecha')

    data_graph = data_frame.groupby('Estación').resample(timeframe).mean()
    data_graph = data_graph.dropna()
    data_graph = data_graph.reset_index()
    data_graph = data_graph[["Estación", "Fecha", "Voltaje Salida Tubo(V)", "Voltaje SHUNT(mV)",  "Corriente Tubo(A)" ]]  
    mode_str =''
    if 'thermo' in params:
        mode_str = 'thermo_csv'
    if 'recti' in params:
        mode_str = 'recti_csv'
    full_path = os.path.dirname(os.path.abspath(__file__))  

    user = query_user(pur)

    owner_id = str(user.owner_id)
    data_graph.to_csv(full_path+'/cathodics_data'+owner_id+'.csv', index=False)
    return  data_graph.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records'), [{"name": i, "id": i} for i in (data_graph.columns.to_list())], 'file.csv?access_token=' + access_token




def history_cathodics_data(req, mode):
    print ('hello history_cathodics_data')
    global data_graph
    global df_cathodics
    total_time = time.time()
    df_cathodics = pd.DataFrame()
    data_graph = pd.DataFrame()

    user = query_user(req)
    if 'thermo' in mode:
        cathodics_data = query_thermo(req)
    if 'recti' in mode:
        cathodics_data = query_recti(req) 
    data_report = pd.concat([cathodics_data])
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
    start_time = time.time()
    print("--- %s creating file' ---" % (time.time() - start_time))

    start_time = time.time()
    full_path = os.path.dirname(os.path.abspath(__file__))  
    data_report.to_csv(full_path+'/cathodics_data'+owner_id+'.csv', index=False)
    print("--- %s creating file csv' ---" % (time.time() - start_time))
    print("--- %s total time' ---" % (time.time() - total_time))

    return data_report

