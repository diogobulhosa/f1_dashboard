import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

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