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

#path = 'https://raw.githubusercontent.com/diogobulhosa/f1_dashboard/main/data/'

df_final = pd.read_csv("./data/cdrcrv2.csv",  sep=',',  encoding='latin-1')
df_points = pd.read_csv("./data/points.csv",header = 0)


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
    ### first part of the page
    html.Div([
        html.Div([
            html.H2('Circuit Information:'),
            html.Div([
                    html.H4('City', style={'font-weight':'bold'}),
                    html.H3(id='circ_city')
                ],className='box_circ_info'),
            html.Div([
                    html.H4('Country', style={'font-weight':'bold'}),
                    html.H3(id='circ_country')
                ],className='box_circ_info'),
            html.Div([
                    html.H4('Years Running', style={'font-weight':'bold'}),
                    html.H3(id='years_running')
                ],className='box_circ_info'),
            html.Div([
                    html.H4('Most Successfull Constructor', style={'font-weight':'bold'}),
                    html.H3(id='circ_msc')
                ],className='box_circ_info'),
            html.Div([
                    html.H4('Most Successfull Driver', style={'font-weight':'bold'}),
                    html.H3(id='circ_msd')
                ],className='box_circ_info'),
            html.Div([
                    html.H4('Pole King', style={'font-weight':'bold'}),
                    html.H3(id='pole_king')
                ],className='box_circ_info')
        ], className='box', style={'width': '30%'}), 
        html.Div([
            html.H2('Chances of watching an accident (%)', style={'text-align':'center'}),
            dcc.Graph(
                id='accident_semi'),
            html.Br(),    
            html.H2('Chances of Pole also winning the race (%)', style={'text-align':'center'}),
            dcc.Graph(
                id='pole_semi'),
                ], className='box', style={'margin-left': '30%','width': '30%'})   
    ],className='circ_box', style={'margin-left': '3%','margin-top': '3%', 'max-height': '700px'}),
    ### Lap Info
    html.Div([
        html.H2('Average Lap Time Evoltuion:'),
        html.H3('This is the average lap-time of the winner. It is important to notice that time behind safety-cars or weather conditions are not taken into consideration.'),
        html.Br(),
        dcc.Graph(
            id='lap-time'
    )], className='box', style={'margin-top': '3%', 'margin-left': '3%'}),   
    ### Winning drivers and Contructors
    html.Div([        
        html.Div([
            html.H2('Winning Drivers:'),
            html.H3('Points accumulated in this circuit.'),

            html.Br(),
            dcc.Graph(
                id='winning-drivers'
            ),
            html.Div([
                html.H2('Number Of Wins by Constructor'),
                html.H3('Click on the Constructor to see how the wins were distributed by each driver'),
                html.Br(),
                dcc.Graph(
                id='winning-constructors')      
            ],className='box', style={'margin-top': '3%','margin-bottom': '10px',
                                        'margin-left': '3%',
                                        'box-shadow': '0px 0px 0px'})
        
        ],className='box', style={'margin-top': '3%',
                                        'margin-left': '3%',
                                        'display': 'table-cell',
                                        'width': '70%', 'box-shadow': '0px 0px 0px'}), 
        html.Div([
                html.Br(),
                html.H3('It is important to notice that the point system as suffered several changes throughout the years.'),
                html.H3('Check in the table bellow every update.'),
                dash_table.DataTable(df_points.to_dict('records'), [{"name": str(i), "id": str(i)} for i in df_points.columns],
                                    style_table={'maxWidth': '20%', 'height':150}, 
                                    style_cell={'fontSize':10},
                                    style_header={'backgroundColor': 'rgb(30, 30, 30)',
                                                  'color': 'white'},
                                    style_data={'backgroundColor': 'rgb(50, 50, 50)',
                                                'color': 'white'},)  
            ], className='box', style={'margin-top': '3%','display': 'table-cell', 'width': '30%', 'box-shadow': '0px 0px 0px','padding-bottom':'10px'})
    ],className='box', style={'margin-top': '3%', 'margin-left': '3%', 'display': 'table', 'padding-bottom':'10px'}),
    #### head to head
    html.Div([
        html.H2('Head to Head', style={'font-weight': 'bold'}),
        html.Label('Analyse Driver or Constructors'),
        dcc.RadioItems(
            id ='dvsc_radio',
            options=['Constructors', 'Drivers'],
            value ='Constructors', inline=True),
        dcc.Dropdown(
            id='dvsc_dropdown1',
            options=[],
            value=['McLaren'],
            multi=True,
            style={'color': 'black', 'background-color':'#d3d3d3'}),            
        ], className='box', style={'margin-top': '3%', 'margin-left': '3%'}),
        html.Div([
            html.Div([
            html.H2('Average Laps'),
            html.H3('Drivers or Constructors who did not finish the race will no appear here.'),
            html.H4('Once again laps behind a safety-car or weather conditions are unfortunely information we do not have, so these are not take into consideration.'),
            html.Br(),
            dcc.Graph(
                id='avg_laps_h2h'
            )], className='box', style={'margin-top': '3%',
                                        'margin-left': '3%',
                                        'display': 'table-cell',
                                        'width': '65%', 'box-shadow': '0px 0px 0px'}), 
            html.Div([
                html.H2('Finishing Races:'),
                html.H3('Here you will be able to observe driver or constructor consistecy in the circuit.'),
                html.Br(),
                dcc.Graph(
                    id='finishing_races'
            )], className='box', style={'margin-top': '3%','display': 'table-cell', 'width': '50%', 'box-shadow': '0px 0px 0px'})
    ],className='box', style={'margin-top': '3%', 'margin-left': '3%', 'display': 'table', })
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

################################CALLBACKFUNCTIONCIRCUITS2############################
@app.callback(
    [Output(component_id='lap-time', component_property='figure'),
     Output(component_id='winning-drivers', component_property='figure'), 
     Output(component_id='winning-constructors', component_property='figure'), 
     Output(component_id='circ_city', component_property='children'), # circ _info call backs start here
     Output(component_id='circ_country', component_property='children'),
     Output(component_id='circ_msd', component_property='children'),
     Output(component_id='circ_msc', component_property='children'),
     Output(component_id='years_running', component_property='children'),
     Output(component_id='pole_king', component_property='children'),
     Output(component_id='pole_semi', component_property='figure'),
     Output(component_id='accident_semi', component_property='figure'),
     Output(component_id='check_update', component_property='children')],
    [Input(component_id="season_slider", component_property='value'),
     Input(component_id="world-map-cricuits", component_property='clickData')]
)

################################CALLBACK2FUNCTIONCIRCUITS############################
def callback_2(year_value, click_map): 
    
    if click_map is None: 
        circuit_value = 'Circuit de Monaco'
        #return dash.no_update  
    else: circuit_value = click_map['points'][0]['text']
    # year loc
    if year_value[0] >= year_value[1]:
        year_value_max = year_value[0]
        year_value_min = year_value[1]
    else: 
        year_value_max = year_value[1]
        year_value_min = year_value[0]
    df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]

    #### Circuit Information ####
    df_final_circuit =  df_seasons.loc[(df_seasons['circuits.name'] == str(circuit_value))]
    
    if len(df_final_circuit)==0:
        update_state = 'Warning: Your circuit did not exist in the chosen seasons, use de slider first and only then the map. Dash will update but use all seasons.'
        year_value_max= 2020
        year_value_min= 1950
        year_value=[1950,2020]
        df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]
        df_final_circuit =  df_seasons.loc[(df_seasons['circuits.name'] == str(circuit_value))]       
    
    else: update_state = 'Circuit Updated'
    
    # City # Country # Most Successful Driver / Constructor # Total Number of DNF # 
    city = df_final_circuit['circuits.location'].unique()[0]
    country = df_final_circuit['circuits.country'].unique()[0]
    msd = df_final_circuit[(df_final_circuit['positionText'] == '1')].groupby('drivers.fullname')['drivers.fullname'].count().sort_values(ascending = False).index.tolist()[0]
    msc = df_final_circuit[(df_final_circuit['positionText'] == '1')].groupby('constructors.name')['constructors.name'].count().sort_values(ascending = False).index.tolist()[0]    
    year_list = (df_final_circuit['races.year'].unique()).tolist()
    year_list.sort()
    year_str = str(year_list)[1:-1]
    pole_name = df_final_circuit[(df_final_circuit['grid'] == 1)].groupby('drivers.fullname',)['drivers.fullname'].count().sort_values(ascending = False).index.tolist()[0]
    pole_count = df_final_circuit[(df_final_circuit['grid'] == 1)].groupby('drivers.fullname',)['drivers.fullname'].count().sort_values(ascending = False)[0]
    pole_king = str(pole_name)+' - '+str(pole_count)
    #### LineChart Best Lap Times ####
    avg_lap_time = df_final_circuit[df_final_circuit['positionText']=='1']
    avg_lap_time['avglaptime'] = avg_lap_time['milliseconds'] / avg_lap_time['laps']
            #gen_fast_lap = df_final_circuit[df_final_circuit['rank']==1]
            #gen_fast_lap['fastestLapTime'] = gen_fast_lap['fastestLapTime'].astype('str').apply(lambda x: time_to_mili(x))
    laptime = px.scatter(avg_lap_time, x="races.year", y="avglaptime",color_discrete_sequence=px.colors.sequential.RdBu, color="drivers.fullname")
    laptime.update_layout(font_color = 'white', paper_bgcolor='rgba(0,0,0,0)', yaxis = {'type': 'date','tickformat': '%M:%S:%ss'},
                      plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Race Year",
                      yaxis_title="Average Lap Time")
    laptime.update_traces(marker=dict(size=18))

    #### Boxplot for winning drivers ####
        #circuit_name = 'Bahrain International Circuit'
        #circuit_value = circuit_name
    driver_points = df_final_circuit.groupby(['drivers.fullname'])['points'].sum().sort_values(ascending = True).nlargest(15).reset_index()
    pointsplot = px.bar(driver_points, x='drivers.fullname', y = 'points', labels={'drivers.fullname':'Drivers Name', 'points': 'Points'}, color_discrete_sequence=px.colors.sequential.RdBu, text='points')
        #fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
        #                  marker_line_width=1.5, opacity=0.6)
    pointsplot.update_traces(textposition='outside',  texttemplate='<b>%{y} Points</b>')
    pointsplot.update_layout(font_color = 'white', paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)')

    #### Pie Chart ####
    contructors =df_final_circuit[(df_final_circuit['circuits.name'] == str(circuit_value)) & (df_final_circuit['positionText'] == '1')].groupby(['constructors.name', 'drivers.surname']).agg({'resultId': 'nunique'})
    contructors.reset_index(inplace = True)
    fig = px.sunburst(contructors, 
                     path=['constructors.name', 'drivers.surname'],
                     values='resultId',color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')    

    # semi_circle
    total_races = len(df_final_circuit['races.year'].unique())
    pole_is_win = len(df_final_circuit[(df_final_circuit['positionText'] == '1') & (df_final_circuit['grid'] == 1)])
    number_accidents = len(df_final_circuit[(df_final_circuit['statusId'] == 3) | (df_final_circuit['statusId'] == 4)])
    race_with_accident = len(df_final_circuit[(df_final_circuit['statusId'] == 3) | (df_final_circuit['statusId'] == 4)].groupby('races.year').count())
    final_accidents = int((round(race_with_accident/total_races, 2))*100)
    final_polewin =int((round(pole_is_win/total_races, 2))*100)

    pole_conv_win = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=final_polewin,
        mode="gauge+number",
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#e50000"}}))
    pole_conv_win.update_layout(
        height = 150,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font_color="white",
        font_size= 15
    )
    accidents_plot = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=final_accidents,
        mode="gauge+number",
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#e50000"}}))
    accidents_plot.update_layout(
        height = 150,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font_color="white",
        font_size= 15
    )



    return laptime, pointsplot, \
           fig, str(city), str(country), str(msd), str(msc),str(year_str), str(pole_king), pole_conv_win, accidents_plot, update_state    

################################CALLBACKFUNCTIONCIRCUITS3############################
@app.callback(
    Output('dvsc_dropdown1', 'options'),
    [Input(component_id='season_slider', component_property='value'),
     Input(component_id="world-map-cricuits", component_property='clickData'),
     Input(component_id='dvsc_radio', component_property='value')
     ]
)
################################CALLBACK3FUNCTIONCIRCUITS############################
def callback_3(year_value, click_map, dvsc_value):
    # year loc
    if click_map is None: 
        circuit_value = 'Circuit de Monaco'
        #return dash.no_update  
    else: circuit_value = click_map['points'][0]['text'] 

    if year_value[0] >= year_value[1]:
        year_value_max = year_value[0]
        year_value_min = year_value[1]
    else: 
        year_value_max = year_value[1]
        year_value_min = year_value[0]
    
    df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]
    df_final_circuit =  df_seasons.loc[(df_seasons['circuits.name'] == str(circuit_value))]
    
    if len(df_final_circuit)==0:
        year_value_max= 2020
        year_value_min= 1950
        year_value=[1950,2020]
        df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]
        df_final_circuit =  df_seasons.loc[(df_seasons['circuits.name'] == str(circuit_value))]       
    
    df_final_circuit['drivers.fullname'] = df_final_circuit[['drivers.forename','drivers.surname']].apply(lambda x: ' '.join(x), axis=1)

    if dvsc_value == 'Drivers':
        return [{'label': c, 'value': c} for c in sorted(df_final_circuit['drivers.fullname'].unique())]
    else: return [{'label': c, 'value': c} for c in sorted(df_final_circuit['constructors.name'].unique())]

################################CALLBACKFUNCTIONCIRCUITS4############################
@app.callback(
     [Output(component_id='finishing_races', component_property='figure'),
     Output(component_id='avg_laps_h2h', component_property='figure') 
     ],
    [Input(component_id='season_slider', component_property='value'),
     Input(component_id="world-map-cricuits", component_property='clickData'),
     Input(component_id="dvsc_radio", component_property='value'),
     Input(component_id='dvsc_dropdown1', component_property='value')
     ]
)
################################CALLBACK4FUNCTIONCIRCUITS############################
def callback_4(year_value, click_map, dvsc_value, client_dc_value):
    # year loc
    if click_map is None: 
        circuit_value = 'Circuit de Monaco'
        #return dash.no_update  
    else: circuit_value = click_map['points'][0]['text'] 
    #circuit_value = click_map['points'][0]['text']
    if year_value[0] >= year_value[1]:
        year_value_max = year_value[0]
        year_value_min = year_value[1]
    else: 
        year_value_max = year_value[1]
        year_value_min = year_value[0]
    
    df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]
    df_final_circuit =  df_seasons.loc[(df_seasons['circuits.name'] == str(circuit_value))]
    
    if len(df_final_circuit)==0:
        year_value_max= 2020
        year_value_min= 1950
        year_value=[1950,2020]
        df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]
        df_final_circuit =  df_seasons.loc[(df_seasons['circuits.name'] == str(circuit_value))]       
    
    df_final_circuit['drivers.fullname'] = df_final_circuit[['drivers.forename','drivers.surname']].apply(lambda x: ' '.join(x), axis=1)

    if dvsc_value == 'Drivers': 
        filter_dc = 'drivers.fullname'
    else: filter_dc = 'constructors.name'
    
    if (client_dc_value is None): 
        return dash.no_update

    ret_list = ['R', 'F', 'W', 'N', 'D','E']
    plot_percentages = pd.DataFrame(columns=[filter_dc,'dnf','firstp','secondp','thirdp','nraces'])
    dc_n_list = df_final_circuit[filter_dc].unique().tolist()
    race_n_list = []
    dnf_n_list = []
    first_n_list = []
    second_n_list = []
    third_n_list = []
    # get n of dnf and n of races and their percentages
    for dc in dc_n_list: 
        race_count = 0
        dnf_count = 0
        first_count = 0
        second_count = 0 
        third_count=0
        for j, dc_name in enumerate(df_final_circuit[filter_dc]):
            if dc == dc_name: 
                if df_final_circuit['positionText'].iloc[j] in ret_list:
                    dnf_count+=1
                elif df_final_circuit['positionText'].iloc[j] == '1':
                    first_count+=1
                elif df_final_circuit['positionText'].iloc[j] == '2':
                    second_count+=1
                elif df_final_circuit['positionText'].iloc[j] == '3':
                    third_count+=1
                race_count+=1

        dnf_n_list.append(dnf_count)
        race_n_list.append(race_count)
        first_n_list.append(first_count)
        second_n_list.append(second_count)
        third_n_list.append(third_count)
    # put them in dataframe
    plot_percentages[filter_dc] = dc_n_list
    plot_percentages.dnf = dnf_n_list
    plot_percentages.nraces = race_n_list
    plot_percentages.firstp=first_n_list
    plot_percentages.secondp=second_n_list
    plot_percentages.thirdp = third_n_list
    # percentage conversion
    plot_percentages['dnf_percentage'] = plot_percentages['dnf'] / plot_percentages['nraces']
    plot_percentages['firstp_percentage'] = plot_percentages['firstp'] / plot_percentages['nraces']
    plot_percentages['secondp_percentage'] = plot_percentages['secondp'] / plot_percentages['nraces']
    plot_percentages['thirdp_percentage'] = plot_percentages['thirdp'] / plot_percentages['nraces']
    plot_percentages['nraces_percentage'] = 1-plot_percentages['dnf_percentage'] - plot_percentages['firstp_percentage']-plot_percentages['secondp_percentage']-plot_percentages['thirdp_percentage']# filtering the drivers client wants 
    pplot_percentages = plot_percentages.loc[plot_percentages[filter_dc].isin(client_dc_value)]
    # number of races
    pplot_percentages[filter_dc] = pplot_percentages[filter_dc].astype('str') +' (' + pplot_percentages['nraces'].astype('str') + ')'
    races_plot = go.Figure()
    races_plot.add_trace(go.Bar(
        y=pplot_percentages[filter_dc],
        x=pplot_percentages['dnf_percentage'],
        name='DNF',
        textposition='inside',
        text = pplot_percentages['dnf'],
        orientation='h',   
        marker=dict(
            color='rgb(153, 0, 0)',
            line=dict(color='DarkGrey', width=1.1)
        )
    ))
    races_plot.add_trace(go.Bar(
        y=pplot_percentages[filter_dc],
        x=pplot_percentages['nraces_percentage'],
        name='No DNF',
        orientation='h',
        textposition='inside',
        text = (pplot_percentages['nraces']-pplot_percentages['dnf']-pplot_percentages['firstp']-pplot_percentages['secondp']-pplot_percentages['thirdp']),
        marker=dict(
            color='rgb(69, 69, 69)',
            line=dict(color='DarkGrey', width=1.1)
        )
    ))  

    races_plot.add_trace(go.Bar(
        y=pplot_percentages[filter_dc],
        x=pplot_percentages['thirdp_percentage'],
        name='Third Position',
        orientation='h',
        textposition='inside',
        text = pplot_percentages['thirdp'],
        marker=dict(
            color='rgb(205, 127, 50)',
            line=dict(color='DarkGrey', width=1.1)
        )
    ))  

    races_plot.add_trace(go.Bar(
        y=pplot_percentages[filter_dc],
        x=pplot_percentages['secondp_percentage'],
        name='Second Position',
        orientation='h',
        textposition='inside',
        text = pplot_percentages['secondp'],
        marker=dict(
            color='rgb(211,211,211)',
            line=dict(color='DarkGrey', width=1.1)
        )
    ))

    
    races_plot.add_trace(go.Bar(
        y=pplot_percentages[filter_dc],
        x=pplot_percentages['firstp_percentage'],
        name='First Position',
        orientation='h',
        textposition='inside',
        text = pplot_percentages['firstp'],
        marker=dict(
            color='rgb(212, 175, 55)',
            line=dict(color='DarkGrey', width=1.1)
        )
    ))

     
    races_plot.update_yaxes(tickfont = dict(size=10))
    races_plot.update_layout(barmode='stack', 
                        plot_bgcolor = 'rgba(0, 0, 0, 0)',
                        paper_bgcolor = 'rgba(0, 0, 0, 0)',  
                        font_color = 'white',  
                        legend=dict(    orientation="h",
                                        yanchor="bottom",
                                        y=1,
                                        xanchor="right",
                                        x=0.95),
                        margin=dict(r=30, t=100, b=70),)
    # Plot for Avg Lap on Head to Head
    dc_avg_lap = df_final_circuit[(df_final_circuit[filter_dc].isin(client_dc_value))&(df_final_circuit['statusId']==1)]
    dc_avg_lap['avglaptime'] = dc_avg_lap['milliseconds'] / dc_avg_lap['laps']
    dc_avg_lap = dc_avg_lap.groupby(['races.year', filter_dc])['avglaptime'].min().reset_index()
    
    avgh2h = px.scatter(dc_avg_lap, x="races.year", y="avglaptime", title='Fastest Lap Time',color_discrete_sequence=px.colors.sequential.RdBu, color=filter_dc)
    avgh2h.update_traces(marker=dict(size=15))
    avgh2h.update_layout(font_color = 'white', paper_bgcolor='rgba(0,0,0,0)', yaxis = {'type': 'date','tickformat': '%M:%S:%ss'},
                        plot_bgcolor='rgba(0,0,0,0)', 
                        xaxis_title="Race Year",
                        yaxis_title="Average Lap Time")
    
    return races_plot, avgh2h

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