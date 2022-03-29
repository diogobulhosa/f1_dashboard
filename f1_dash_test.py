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
        html.Label('Choose a Circuit:'),
        dcc.Dropdown(
        id='drop',
        options=options,
        value='Albert Park Grand Prix Circuit'
    ),
    dcc.Graph(
        id='example-graph'
    )], className='box', style={'margin': '100px', 'margin-left': '40%', 'padding-top':'15px', 'padding-bottom':'105px'}),    


])


@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='drop', component_property='value')]
)
def callback_1(input_value):
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


if __name__ == '__main__':
    app.run_server(debug=True)