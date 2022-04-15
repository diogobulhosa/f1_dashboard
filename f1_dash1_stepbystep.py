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

tab_circuits =  html.Div([
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

tab_pilots =  html.Div([
    html.Div([
        html.H2('Choose one driver', style={'font-weight': 'bold'}),
        html.H3('Choose one driver you would like to know more about'),
        dcc.Dropdown(
            id='driver_dropdown2',
            options=df_final['drivers.fullname'].unique(),
            value='Lewis Hamilton',
            multi=False, 
            style={'color': 'black', 'background-color':'#d3d3d3'})         
        ], className='box', style={'margin-top': '3%', 'margin-left': '3%'}),
        html.Div([
            html.Div([
                html.H2('Driver Information:'),
                html.Div([
                        html.H4('Country', style={'font-weight':'bold'}),
                        html.H3(id='driver-country')
                    ],className='box_circ_info'),
                html.Div([
                        html.H4('Number of Podiums', style={'font-weight':'bold'}),
                        html.H3(id='npodiums')
                    ],className='box_circ_info'),
                html.Div([
                        html.H4('Carreer Points', style={'font-weight':'bold'}),
                        html.H3(id='carreerpoints')
                    ],className='box_circ_info'),
                html.Div([
                        html.H4('Races Entered', style={'font-weight':'bold'}),
                        html.H3(id='races_entered')
                    ],className='box_circ_info'),
                html.Div([
                        html.H4('Highest Race Finish', style={'font-weight':'bold'}),
                        html.H3(id='highest_race_finish')
                    ],className='box_circ_info'),
                html.Div([
                        html.H4('Highest Grid Start', style={'font-weight':'bold'}),
                        html.H3(id='highest_grid')
                    ],className='box_circ_info'),
                html.Div([
                        html.H4('Number of Retirements', style={'font-weight':'bold'}),
                        html.H3(id='naccidents')
                    ],className='box_circ_info')
                ], className='box', style={'margin-top': '3%',
                                        'margin-left': '3%',
                                        'display': 'table-cell',
                                        'width': '65%', 'box-shadow': '0px 0px 0px'}), 
            html.Div([
                html.H2('Constructors the Driver as Represented'),
                html.Br(),
                dcc.Graph(
                    id='driver-const')
                ], className='box', style={'margin-top': '3%','display': 'table-cell', 'width': '50%', 'box-shadow': '0px 0px 0px'})
        ],className='box', style={'margin-top': '3%', 'margin-left': '3%', 'display': 'table', }),

        html.Div([
            html.H2('Carreer Finishes'),
            html.H3('The Positions are between 1-20, the 21th position refers to DNF.'),
            dcc.Graph(
                id='race-finish'),                
        ], className='box', style={'margin-top': '3%', 'margin-left': '3%'}),
         html.Div([
            html.H2('Total Points Each Season'),
            dcc.Graph(
                id='points-season'),                
        ], className='box', style={'margin-top': '3%', 'margin-left': '3%'}),
], className='main')


app.layout = dbc.Container([ 
        html.Div([
            html.Img(src=app.get_asset_url('formula-1-logo-7.png'), style={'width': '100%', 'margin-top': '3%'}),
            html.H1(children='F1 DASH', style={'position': 'relative','top': '2%'}),
            html.Label('A Dashboard for a more comprehensive insight throughout years and years of the best racing there is.', 
                        style={'color':'#e1e2df'}),
            html.H3('Dashboard by: Diogo Bulhosa, Francisco Costa, Mafalda Figueiredo, Rodrigo Pimenta', 
                        style={'color':'#e1e2df', 'position': 'absolute', 'bottom': '0', 'left':'0'})
        ], className='side_bar'),
        
        html.Div([
            dbc.Tabs([
                    dbc.Tab(tab_circuits, label="Circuits", labelClassName ='labels', tabClassName = 'tabs'),
                    dbc.Tab(tab_pilots, label="Pilots", labelClassName ='labels', tabClassName = 'tabs', tab_style={'margin-left' : '0%'}),
                ])
        ],className='boxtabs', style={'margin-top': '3%', 'margin-left': '15%'}),
    ],
    fluid=True,
)

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
@app.callback(
    [Output(component_id='race-finish', component_property='figure'),
     Output(component_id='points-season', component_property='figure'),
     Output(component_id='driver-const', component_property='figure'),
     Output(component_id='driver-country', component_property='children'), # circ _info call backs start here
     Output(component_id='npodiums', component_property='children'),
     Output(component_id='carreerpoints', component_property='children'),
     Output(component_id='races_entered', component_property='children'),
     Output(component_id='highest_race_finish', component_property='children'),
     Output(component_id='highest_grid', component_property='children'),
     Output(component_id='naccidents', component_property='children'),
     ],
    Input(component_id="driver_dropdown2", component_property='value')
)

def callback_5(client_driver):
    if not client_driver: 
        client_driver='Lewis Hamilton'

    driver_nationality = df_final[df_final['drivers.fullname']==client_driver]['drivers.nationality'].iloc[0]
    podium_pos = ['1','2','3']
    npodiums = len(df_final[(df_final['drivers.fullname']==client_driver) & (df_final['positionText'].isin(podium_pos))])
    npoints = df_final[(df_final['drivers.fullname']==client_driver)].groupby('drivers.fullname')['points'].sum().reset_index()['points'].iloc[0]
    nraces = len(df_final[(df_final['drivers.fullname']==client_driver)])
    ret_list = ['R', 'F', 'W', 'N', 'D','E']
    race_serie = df_final[(df_final['drivers.fullname']==client_driver) & ~(df_final['positionText'].isin(ret_list))]['positionText']
    highest_rf = race_serie.astype(int).min()
    highest_grid_start = df_final[(df_final['drivers.fullname']==client_driver)]['grid'].min()
    number_ret = len(df_final[(df_final['drivers.fullname']==client_driver) & (df_final['positionText'].isin(ret_list))])
    ##### Position Scatter ######
    df_pos = df_final[(df_final['drivers.fullname']==client_driver)]
    df_pos = df_pos.groupby(['races.year', 'races.round','positionText']).count().reset_index()
    df_pos['posTextInt'] = df_pos["positionText"].map(lambda x: '21' if x in ret_list else x)  
    df_pos['round_year'] = df_pos['races.round'].astype(str) + ' ' + df_pos['races.year'].astype(str)
    driver_position = px.scatter(df_pos, x="round_year", y="posTextInt")
    driver_position.update_layout(font_color = 'white', paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Race Year",
                      yaxis_title="Position")
    driver_position.update_yaxes(autorange="reversed"),                 
    driver_position.update_traces(marker=dict(size=5, color='red'))

    #### Point Progress ####
    driver_points_gen = df_final[(df_final['drivers.fullname']==client_driver)].groupby('races.year')['points'].sum().reset_index()

    pointsplot = px.bar(driver_points_gen, x='races.year', y = 'points', labels={'races.year':'Season', 'points': 'Points'}, color_discrete_sequence=px.colors.sequential.RdBu, text='points')
    pointsplot.update_traces(textposition='outside',  texttemplate='<b>%{y} Points</b>')
    pointsplot.update_layout(font_color = 'white', paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)')

    #### Constructor Driver ####
    driv_const = df_final[(df_final['drivers.fullname']==client_driver)].groupby(['drivers.fullname','constructors.name'])['raceId'].count().reset_index()
    driver_const = px.pie(driv_const, values='raceId', names='constructors.name',color_discrete_sequence=px.colors.sequential.RdBu,width=650, height=325)
    driver_const.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color = 'white',
                      plot_bgcolor='rgba(0,0,0,0)')  
    
    return driver_position, pointsplot, driver_const, str(driver_nationality), str(npodiums), str(npoints), str(nraces), str(highest_rf), str(highest_grid_start), str(number_ret)



if __name__ == '__main__':
    app.run_server(debug=True)