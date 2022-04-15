from http import client
from pydoc import classname
from turtle import color
import dash
from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

df_final = pd.read_csv("cdrcrv2.csv",  sep=',',  encoding='latin-1')
df_points = pd.read_csv('https://raw.githubusercontent.com/diogobulhosa/f1_dashboard/main/data/points.csv',header = 0)



app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
    dcc.Input(id='input',
              value='initial value',
              type='text'),
    html.Div(id='div')
])


@app.callback(
    Output(component_id='div', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)