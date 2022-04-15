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
import warnings
import dash_bootstrap_components as dbc
warnings.filterwarnings("ignore")

# Dataset Processing
df_final = pd.read_csv("cdrcrv2.csv",  sep=',',  encoding='latin-1')
df_points = pd.read_csv('https://raw.githubusercontent.com/diogobulhosa/f1_dashboard/main/data/points.csv',header = 0)


df_final['drivers.fullname'] = df_final[['drivers.forename','drivers.surname']].apply(lambda x: ' '.join(x), axis=1)
df_final['drivers.fullname'] = df_final[['drivers.forename','drivers.surname']].apply(lambda x: ' '.join(x), axis=1)
df_final['points'] = df_final['points'].astype(int)
df_final['races.year'] = df_final['races.year'].astype(int)
df_final.replace('\\N','0', inplace=True)
df_final['milliseconds'] = df_final['milliseconds'].astype(int)# Requirements for the dash core components

circuit_options = [
    dict(label=circuit, value=circuit)
    for circuit in df_final['circuits.name'].unique()]

# pedir oinião prof df_final['races.year'].max()
#  value=[df_final['races.year'].min(), df_final['races.year'].max()]
season_slider = dcc.RangeSlider(
        id='season_slider',
        min=df_final['races.year'].min(),
        max=df_final['races.year'].max(),
        tooltip={"placement": "bottom", "always_visible": True},
        marks={str(i): '{}'.format(str(i)) for i in
               list(range(1950,2021,5))},
        value=[df_final['races.year'].min(), df_final['races.year'].max()],
        step=1
    )

def time_to_mili(s):
    hours, minutes, seconds = (["0", "0"] + s.split(":"))[-3:]
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds)
    miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
    return miliseconds

# The App itself

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div([
    ### choose circuit main information
    html.Div([
        html.Div([
            html.H2('Choose a Circuit:',style={'font-weight': 'bold'} ),
            html.H4('Click on one of the red dots in the Map to select a circuit. (default: Circuit de Monaco)'),
            html.Br(),
            html.Label('Choose seasons'),
            season_slider,  
            html.Br(),
            dcc.Graph(
                id='world-map-cricuits'),
            html.Br(),
            html.H3(id='check_update',style={'font-weight':'bold', 'margin-down':'0%'})], className='box', style={'margin-top': '3%'})
    ],style={'margin-left': '3%'}),
], className='main')



################################CALLBACK############################################

@app.callback(
    Output(component_id='world-map-cricuits', component_property='figure'),
    [Input('season_slider', 'value')]
)

################################CALLBACKFUNCTIONCIRCUITS############################
# recebe os years, retorna o grafico+lista de circuitos available nessa altura
def callback_1(year_value):
    # check which value is higher
    if year_value[0] >= year_value[1]:
        year_value_max = year_value[0]
        year_value_min = year_value[1]
    else: 
        year_value_max = year_value[1]
        year_value_min = year_value[0]

    # create dataset
    df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]


    data_scattergeo = dict(type='scattergeo', 
                        lat=df_seasons['circuits.lat'], 
                        lon=df_seasons['circuits.lng'],
                        
                        mode=['markers','text'][0],
                        text=df_seasons['circuits.name'],
                        marker=dict(color='firebrick',
                                    size=7
                                    )
                        )
                        
    layout_scattergeo = dict(geo=dict(scope='world',  #default
                                          projection=dict(type='equirectangular'
                                                         ),
                                          #showland=True,   #default
                                          showocean=True,
                                          landcolor='seagreen',
                                          lakecolor='cornflowerblue',
                                          oceancolor='royalblue'
                                         ),
                                
                                margin = dict(t = 30, b = 0, l = 0, r=0, pad=0),

                                title=dict(text='Circuits Around the World',
                                           font_color = '#e1e2df', 
                                           x=.5 # Title relative position according to the xaxis, range (0,1)
                                           ),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)'
                                )
    return go.Figure(data=data_scattergeo, layout=layout_scattergeo)

################################CALLBACKTABDRIVERS############################



if __name__ == '__main__':
    app.run_server(debug=True)