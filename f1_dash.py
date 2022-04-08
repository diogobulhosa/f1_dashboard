import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px

# Dataset Processing

path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/Lesson_1/'

df_final = pd.read_excel('./data/cdrcr.xlsx')


geo_path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/Lesson_4/'
import urllib.request, json 

with urllib.request.urlopen(geo_path + 'countries.geojson') as url:
        data_geo = json.loads(url.read().decode())

for feature in data_geo['features']:
        feature['id'] = feature['properties']['ADMIN']  

# Requirements for the dash core components

circuit_options = [
    dict(label=circuit, value=circuit)
    for circuit in df_final['circuits.name'].unique()]

# pedir oinião prof df_final['races.year'].max()
#  value=[df_final['races.year'].min(), df_final['races.year'].max()]
season_slider = dcc.RangeSlider(
        id='season_slider',
        min=df_final['races.year'].min(),
        max=2020,
        marks={str(i): '{}'.format(str(i)) for i in
               list(range(1950,2021,5))},
        value=[df_final['races.year'].min(), df_final['races.year'].max()],
        step=1
    )
"""    
dropdown_circuits = dcc.Dropdown(
        id='circuit_drop',
        options=[],
        value=['']
    )
"""

def time_to_mili(s):
    hours, minutes, seconds = (["0", "0"] + s.split(":"))[-3:]
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds)
    miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
    return miliseconds

# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    # side bar 
    html.Div([
        html.Img(src=app.get_asset_url('formula-1-logo-7.png'), style={'width': '100%', 'top': '5%'}),
        html.H1(children='F1 DASH', style={'position': 'relative','top': '2%'}),
        html.Label('A Dashboard for a more comprehensive insight throughout years and years of the best racing there is.', 
                    style={'color':'rgb(65 65 65)'})
    ], className='side_bar'),

    # choose circuit main information
    html.Div([
        html.Div([
            html.H1('Choose a Circuit:'),
            html.Label('Choose seasons'),
            season_slider,  
            html.Br(),
            dcc.Graph(
                id='world-map-cricuits'
        )], className='box', style={'margin-top': '3%'})

    ],style={'margin-left': '3%'}),

    html.Div([
        html.H2('Circuit Information:'),
        html.Div([
                html.H4('City', style={'font-weight':'lighter'}),
                html.H3(id='circ_city')
            ],className='box_circ_info'),
        html.Div([
                html.H4('Country', style={'font-weight':'lighter'}),
                html.H3(id='circ_country')
            ],className='box_circ_info'),
        html.Div([
                html.H4('Most Successfull Driver', style={'font-weight':'lighter'}),
                html.H3(id='circ_msd')
            ],className='box_circ_info'),
        html.Div([
                html.H4('Most Successfull Constructor', style={'font-weight':'normal'}),
                html.H3(id='circ_msc')
            ],className='box_circ_info'),
        html.Div([
                html.H4('Number of Accidents', style={'font-weight':'normal'}),
                html.H3(id='number_accidents')
            ],className='box_circ_info')
    ], className='box', style={'margin-top': '3%', 'margin-left': '5%'}), 
    
    html.Div([
        html.H2('Fastest Lap Time Evoltuion:'),
        html.Br(),
        dcc.Graph(
            id='lap-time'
    )], className='box', style={'margin-top': '3%', 'margin-left': '20%'}),   

    html.Div([
        html.H2('Winning Drivers:'),
        html.Br(),
        dcc.Graph(
            id='winning-drivers'
    )], className='box', style={'margin-top': '3%', 'margin-left': '20%'}), 

    html.Div([
        html.H2('Winning Constructors:'),
        html.Br(),
        dcc.Graph(
            id='winning-constructors'
    )], className='box', style={'margin-top': '3%', 'margin-left': '20%'}), 

    html.Div([
        html.H1('Head to Head'),
        html.Label('Analyse Driver or Constructors'),
        dcc.RadioItems(
            id ='dvsc_radio',
            options=['Drivers', 'Constructors'],
            value ='Drivers', inline=True),
        dcc.Dropdown(
            id='dvsc_dropdown1',
            options=[],
            multi=True),            
        ], className='box', style={'margin-top': '3%', 'margin-left': '20%'}),

    html.Div([
        html.H1('Finished Races'),
        dcc.Graph(
            id='finishing_races')
    ],className='box', style={'margin-top': '3%', 'margin-left': '20%'}),

], className='main')

################################CALLBACK############################################

@app.callback(
    Output(component_id='world-map-cricuits', component_property='figure'),
    [Input('season_slider', 'value')]
)

################################CALLBACKFUNCTIONCIRCUITS############################
# recebe os years, retorna o grafico+lista de circuitos available nessa altura
def callback_1(year_value):
    print(year_value)

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
                        marker=dict(color='red',
                                    size=7
                                    )
                        )

    layout_scattergeo = dict(geo=dict(scope='world',  #default
                                          projection=dict(type='equirectangular'
                                                         ),
                                          #showland=True,   #default
                                          landcolor='black',
                                          lakecolor='white'
                                         ),
                                
                                margin = dict(t = 0, b = 0, l = 0, r=0),

                                title=dict(text='Circuits Around the World',
                                            x=.5 # Title relative position according to the xaxis, range (0,1)
                                           )
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
     Output(component_id='number_accidents', component_property='children')],
    [Input(component_id="season_slider", component_property='value'),
     Input(component_id="world-map-cricuits", component_property='clickData')]
)

################################CALLBACK2FUNCTIONCIRCUITS############################
def callback_2(year_value, click_map): 
    if click_map is None: 
        return dash.no_update  
    circuit_value = click_map['points'][0]['text']
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
    df_final_circuit['drivers.fullname'] = df_final_circuit[['drivers.forename','drivers.surname']].apply(lambda x: ' '.join(x), axis=1)

    # City # Country # Most Successful Driver / Constructor # Total Number of DNF # 
    city = df_final_circuit['circuits.location'].unique()[0]
    country = df_final_circuit['circuits.country'].unique()[0]
    msd = df_final_circuit[(df_final_circuit['circuits.name'] == str(circuit_value)) & (df_final_circuit['positionText'] == 1)].groupby('drivers.fullname')['drivers.fullname'].count().sort_values(ascending = False).index.tolist()[0]
    msc = df_final_circuit[(df_final_circuit['circuits.name'] == str(circuit_value)) & (df_final_circuit['positionText'] == 1)].groupby('constructors.name')['constructors.name'].count().sort_values(ascending = False).index.tolist()[0]    
    number_accidents = len(df_final_circuit[(df_final_circuit['statusId'] == 3) | (df_final_circuit['statusId'] == 4)])
    #### LineChart Best Lap Times ####
    gen_fast_lap = df_final_circuit[df_final_circuit['rank']==1]
    gen_fast_lap['fastestLapTime'] = gen_fast_lap['fastestLapTime'].astype('str').apply(lambda x: time_to_mili(x))
    laptime = px.scatter(gen_fast_lap, x="races.year", y="fastestLapTime", title='Fastest Lap Time',color_discrete_sequence=px.colors.sequential.RdBu, color="drivers.fullname", symbol="drivers.fullname")
    laptime.update_layout(font_color = 'white', paper_bgcolor='rgba(0,0,0,0)', yaxis = {'type': 'date','tickformat': '%M:%S:%ss'},
                      plot_bgcolor='rgba(0,0,0,0)')

    #### Boxplot for winning drivers
    #circuit_name = 'Bahrain International Circuit'
    #circuit_value = circuit_name
    driver_points = df_final_circuit.groupby(['drivers.fullname'])['points'].sum().sort_values(ascending = True).nlargest(15).reset_index()
    pointsplot = px.bar(driver_points, x='drivers.fullname', y = 'points', labels={'drivers.fullname':'Drivers Name', 'points': 'Points'}, color_discrete_sequence=px.colors.sequential.RdBu, text='points')
    #fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
    #                  marker_line_width=1.5, opacity=0.6)
    pointsplot.update_traces(textposition='outside',  texttemplate='<b>%{y} Points</b>')
    pointsplot.update_layout(font_color = 'white', paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)')

    #### Pie Chart 
    contructors =df_final_circuit[(df_final_circuit['circuits.name'] == str(circuit_value)) & (df_final_circuit['positionText'] == 1)].groupby(['constructors.name', 'drivers.surname']).agg({'resultId': 'nunique'})
    contructors.reset_index(inplace = True)
    fig = px.sunburst(contructors, 
                     path=['constructors.name', 'drivers.surname'],
                     values='resultId',color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
    return laptime, pointsplot, \
           fig, str(city), str(country), str(msd), str(msc),str(number_accidents)    

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
        return dash.no_update  
    circuit_value = click_map['points'][0]['text']
    if year_value[0] >= year_value[1]:
        year_value_max = year_value[0]
        year_value_min = year_value[1]
    else: 
        year_value_max = year_value[1]
        year_value_min = year_value[0]
    
    df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]
    df_final_circuit =  df_seasons.loc[(df_seasons['circuits.name'] == str(circuit_value))]
    df_final_circuit['drivers.fullname'] = df_final_circuit[['drivers.forename','drivers.surname']].apply(lambda x: ' '.join(x), axis=1)

    if dvsc_value == 'Drivers':
        return [{'label': c, 'value': c} for c in sorted(df_final_circuit['drivers.fullname'].unique())]
    else: return [{'label': c, 'value': c} for c in sorted(df_final_circuit['constructors.name'].unique())]

################################CALLBACKFUNCTIONCIRCUITS4############################
@app.callback(
    Output(component_id='finishing_races', component_property='figure'),
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
        return dash.no_update  
    circuit_value = click_map['points'][0]['text']
    if year_value[0] >= year_value[1]:
        year_value_max = year_value[0]
        year_value_min = year_value[1]
    else: 
        year_value_max = year_value[1]
        year_value_min = year_value[0]
    
    df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]
    df_final_circuit =  df_seasons.loc[(df_seasons['circuits.name'] == str(circuit_value))]
    df_final_circuit['drivers.fullname'] = df_final_circuit[['drivers.forename','drivers.surname']].apply(lambda x: ' '.join(x), axis=1)

    if dvsc_value == 'Drivers': 
        filter_dc = 'drivers.fullname'
    else: filter_dc = 'constructors.name'

    if (client_dc_value is None): 
        return dash.no_update

    print(client_dc_value)
    ret_list = ['R', 'F', 'W', 'N', 'D','E']
    plot_percentages = pd.DataFrame(columns=[filter_dc,'dnf','nraces'])
    dc_n_list = df_final_circuit[filter_dc].unique().tolist()
    race_n_list = []
    dnf_n_list = []
    # get n of dnf and n of races and their percentages
    for dc in dc_n_list: 
        race_count = 0
        dnf_count = 0
        for j, dc_name in enumerate(df_final_circuit[filter_dc]):
            if dc == dc_name: 
                if df_final_circuit['positionText'].iloc[j] in ret_list:
                    dnf_count+=1
                race_count+=1
        dnf_n_list.append(dnf_count)
        race_n_list.append(race_count)    
    # put them in dataframe
    plot_percentages[filter_dc] = dc_n_list
    plot_percentages.dnf = dnf_n_list
    plot_percentages.nraces = race_n_list
    # percentage conversion
    plot_percentages['dnf_percentage'] = plot_percentages['dnf'] / plot_percentages['nraces']
    plot_percentages['nraces_percentage'] = 1-plot_percentages['dnf_percentage']
    # filtering the drivers client wants 
    pplot_percentages = plot_percentages.loc[plot_percentages[filter_dc].isin(client_dc_value)]
    races_plot = go.Figure()
    races_plot.add_trace(go.Bar(
        y=pplot_percentages[filter_dc],
        x=pplot_percentages['dnf_percentage'],
        name='DNF',
        orientation='h',   
        marker=dict(
            color='rgba(153, 0, 0, 0.6.0)',
            line=dict(color='rgba(153, 0, 0, 1.0)', width=1)
        )
    ))
    races_plot.add_trace(go.Bar(
        y=pplot_percentages[filter_dc],
        x=pplot_percentages['nraces_percentage'],
        name='No DNF',
        text=pplot_percentages['nraces'],
        textposition='outside',
        orientation='h',
        marker=dict(
            color='rgba(69, 69, 69, 0.6)',
            line=dict(color='rgba(0, 0, 0, 1)', width=1)
        )
    ))

    races_plot.update_layout(barmode='stack')

    return races_plot



if __name__ == '__main__':
    app.run_server(debug=True)