import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Dataset Processing

path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/Lesson_1/'

df_final = pd.read_excel('./data/circuits_drivers_races_results.xlsx')



# Requirements for the dash core components

options = country_options = [
    dict(label=circuit, value=circuit)
    for circuit in df_final['circuits.name'].unique()]

season_slider = dcc.RangeSlider(
        id='season_slider',
        min=df_final['races.year'].min(),
        max=df_final['races.year'].max(),
        marks={str(i): '{}'.format(str(i)) for i in
               [1950, 1960, 1980, 1990, 2000, 2010, 2020]},
        value=[df_final['races.year'].min(), df_final['races.year'].max()],
        step=1
    )

# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

     html.Div([
        html.Img(src=app.get_asset_url('formula-1-logo-7.png'), style={'width': '100%', 'top': '5%'}),
        html.H1(children='F1 DASH', style={'position': 'relative','top': '2%'}),
        html.Label('A Dashboard for a more comprehensive insight throughout years and years of the best racing there is.', 
                    style={'color':'rgb(65 65 65)'})
    ], className='side_bar'),

    html.Div([
        html.H1('Choose a Circuit:'),
        html.Label('Choose seasons'),
        season_slider,  
        html.Br(),
        dcc.Graph(
            id='world-map-cricuits'
    )], className='box', style={'margin': '15%', 'margin-left': '20%'}),    


])

################################CALLBACK############################################

@app.callback(
    Output(component_id='world-map-cricuits', component_property='figure'),
    [Input(component_id="season_slider", component_property='value')]
)

################################CALLBACKFUNCTIONCIRCUITS############################
def callback_1(year_value):
    """""
    data_bar = dict(type='bar',
                    y=df_final[(df_final['circuits.name'] == input_value) & (df_final['positionText'] == 1)].groupby('drivers.surname')['drivers.surname'].count().sort_values(ascending = False).tolist(),
                    x=df_final[(df_final['circuits.name'] == input_value) & (df_final['positionText'] == 1)].groupby('drivers.surname')['drivers.surname'].count().sort_values(ascending = False).index.tolist(),
                    texttemplate='<b>%{y} Wins</b>',
                    textposition='outside'
                    )

    layout_bar = dict(yaxis=dict(range=(0, 10),
                                 title='Number of Wins'
                                 )
                      )

    return go.Figure(data=data_bar, layout=layout_bar)
"""
    # check which value is higher
    if year_value[0] >= year_value[1]:
        year_value_max = year_value[0]
        year_value_min = year_value[1]
    else: 
        year_value_max = year_value[1]
        year_value_min = year_value[0]

    # create dataset
    df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]


    geo_path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/Lesson_4/'
    import urllib.request, json 

    with urllib.request.urlopen(geo_path + 'countries.geojson') as url:
        data_geo = json.loads(url.read().decode())

    for feature in data_geo['features']:
        feature['id'] = feature['properties']['ADMIN']  


    data_scattergeo = dict(type='scattergeo', 
                        lat=df_seasons['circuits.lat'], 
                        lon=df_seasons['circuits.lng'],
                        
                        mode=['markers','text'][0],
                        text=df_seasons['circuits.name'],
                        marker=dict(color='red',
                                    size=7
                                    )
                        )
    """"
    layout_scattermap = dict(mapbox=dict(style='white-bg',
                                        layers=[dict(source=feature,
                                                    below='traces',
                                                    type='fill',
                                                    fill=dict(outlinecolor='gray')
                                                            ) for feature in data_geo['features']]
                                        ),
                            title=dict(text='World Map',
                                        x=.5 # Title relative position according to the xaxis, range (0,1)
                                    )
                            )
    return go.Figure(data=data_scattermap, layout=layout_scattermap)
    """
    layout_scattergeo = dict(geo=dict(scope='world',  #default
                                          projection=dict(type='equirectangular'
                                                         ),
                                          #showland=True,   #default
                                          landcolor='black',
                                          lakecolor='white'
                                         ),

                                 title=dict(text='Circuits Around the World',
                                            x=.5 # Title relative position according to the xaxis, range (0,1)
                                           )
                                )
    return go.Figure(data=data_scattergeo, layout=layout_scattergeo)
    
if __name__ == '__main__':
    app.run_server(debug=True)