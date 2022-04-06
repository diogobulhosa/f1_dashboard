import dash  # Dash 1.16 or higher
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
# need to pip install statsmodels for trendline='ols' in scatter plot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Data from U.S. Congress, Joint Economic Committee, Social Capital Project. https://www.jec.senate.gov/public/index.cfm/republicans/2018/4/the-geography-of-social-capital-in-america
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Callbacks/chained_callback/social-capital-project.csv")

df_final = pd.read_excel('./data/circuits_drivers_races_constructors_results.xlsx')

app.layout = html.Div([
    html.Label("State:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id='states-dpdn',
        options=[{'label': s, 'value': s} for s in sorted(df.State.unique())],
        value='Alaska',
        clearable=False
    ),

    html.H1('Choose a Circuit:'),
    html.Label('Choose seasons'),
    dcc.RangeSlider(
        id='season_slider',
        min=df_final['races.year'].min(),
        max=df_final['races.year'].max(),
        marks={str(i): '{}'.format(str(i)) for i in
               [1950, 1960, 1980, 1990, 2000, 2010, 2020]},
        value=[df_final['races.year'].min(), df_final['races.year'].max()],
        step=1
    ), 

    html.Label("Counties:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(id='counties-dpdn', options=[], multi=True),

    html.Label('Circuit Choice'),
    dcc.Dropdown(
        id='circuit_drop',
        options=[]
    ),

    dcc.Graph(id='display-map', figure={})
])


# Populate the options of counties dropdown based on states dropdown
@app.callback(
    Output('counties-dpdn', 'options'),
    Input('states-dpdn', 'value')
)
def set_cities_options(chosen_state):
    dff = df[df.State==chosen_state]
    return [{'label': c, 'value': c} for c in sorted(dff.County.unique())]

@app.callback(
    Output('circuit_drop', 'options'),
    Input('season_slider', 'value')
)
def set_circuit_options(chosen_seasons):
     # check which value is higher
    if chosen_seasons[0] >= chosen_seasons[1]:
        year_value_max = chosen_seasons[0]
        year_value_min = chosen_seasons[1]
    else: 
        year_value_max = chosen_seasons[1]
        year_value_min = chosen_seasons[0]

    # create dataset
    df_seasons = df_final.loc[(df_final['races.year'] <= year_value_max) & (df_final['races.year'] >= year_value_min)]
    return [{'label': c, 'value': c} for c in sorted(df_seasons['circuits.name'].unique())]


# populate initial values of counties dropdown
@app.callback(
    Output('counties-dpdn', 'value'),
    Input('counties-dpdn', 'options')
)
def set_cities_value(available_options):
    return [x['value'] for x in available_options]


@app.callback(
    Output('display-map', 'figure'),
    Input('counties-dpdn', 'value'),
    Input('states-dpdn', 'value')
)
def update_grpah(selected_counties, selected_state):
    if len(selected_counties) == 0:
        return dash.no_update
    else:
        dff = df[(df.State==selected_state) & (df.County.isin(selected_counties))]

        fig = px.scatter(dff, x='% without health insurance', y='% in fair or poor health',
                         color='% adults graduated high school',
                         size='bubble_size',
                         hover_name='County',
                         # hover_data={'bubble_size':False},
                         labels={'% adults graduated high school':'% graduated high school',
                                 '% without health insurance':'% no health insurance',
                                 '% in fair or poor health':'% poor health'}
                         )
        return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)


