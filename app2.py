import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
from flask import Flask

df = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')





#df[' index'] = range(1, len(df) + 1)
app = dash.Dash()
application = app.server

PAGE_SIZE = 5

app.layout = dt.DataTable(
    id='datatable-paging',
    columns=[
        {"name": i, "id": i} for i in sorted(df.columns)
    ],
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom'
)

@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
     Input('datatable-paging', "page_size")])

def update_table(page_current,page_size):
    return df.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

if __name__ == '__main__':
    application.run(debug=False, port=8080)