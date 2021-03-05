import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
#https://www.allmusic.com/album/rumours-mw0000193833

import pandas as pd
import numpy as np

#df = pd.read_csv('LotsOMusic/data.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#print(df.columns)
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)


url_bar_and_content_div = html.Div([ #is this a hidden div?
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.H2('Welcome'),
    html.P("Hello my name is George Mazzeo im a little baby bitch boy who really needs to grow up and get a job"),

])

'''layout_index = html.Div([
    dcc.Link('Navigate to "/Welcome"', href='/Welcome'),
    html.Br(),
    dcc.Link('Navigate to "/MyCoolApp"', href='/MyCoolApp'),
])'''

layout_welcome = html.Div([])



layout_my_app = html.Div([
    html.H2('My Cool App'),
    dcc.Dropdown(
        id='MyCoolApp-dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='MyCoolApp-display-value'),
    html.Br(),

    html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            #min=df['year'].min(),
            #max=df['year'].max(),
            #value=df['year'].min(),
            #marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        )
    ]),

    #dcc.Link('Navigate to "/Welcome"', href='/Welcome'),
])

# index layout
app.layout = url_bar_and_content_div



# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    #layout_welcome,
    layout_my_app,
])


# Index callbacks
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              [dash.dependencies.Input('submit-val', 'n_clicks')],
              [dash.dependencies.State('input-on-submit', 'value')])
def display_page(pathname,n_clicks,value):
    print(value)
    if value == 'this is a joke':
        return layout_my_app

    if pathname == "/Welcome":
        return layout_welcome
    elif pathname == "/MyCoolApp":
        return layout_my_app
    else:
        return layout_welcome


# Welcome Page 1 callbacks
# @app.callback(
#     dash.dependencies.Output('container-button-basic', 'children'),
#     [dash.dependencies.Input('submit-val', 'n_clicks')],
#     [dash.dependencies.State('input-on-submit', 'value')])
# def update_output(n_clicks, value):
#     print(value)
#     if value == 'this is a joke':
#         display_value("/MyCoolApp")
#
#     return 'The input value was "{}" and the button has been clicked {} times'.format(
#         value,
#         n_clicks
#     )



# Page 2 callbacks
@app.callback(Output('MyCoolApp-display-value', 'children'),
              Input('MyCoolApp-dropdown', 'value'))
def display_value(value):
    #print('display_value')
    return 'You have selected "{}"'.format(value)


# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     Input('year-slider', 'value'))
# def update_figure(selected_year):
#     #filtered_df = df[df.year == selected_year]
#
#     #fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
#                      #size="pop", color="continent", hover_name="country",
#                      #log_x=True, size_max=55)
#
#     #fig.update_layout(transition_duration=500)
#
#     return #fig


if __name__ == '__main__':
    app.run_server(debug=True)
