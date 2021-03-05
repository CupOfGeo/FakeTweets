import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.express as px
import json


import flask

app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div(id='output-state'),
    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Button(id='submit-button', n_clicks=0, children='Submit')
])

@app.callback(Output('intermediate-value', 'children'), Input('submit-button', 'n_clicks'))
def clean_data(n_clicks):

     score = [n_clicks,2,3,4]

     return json.dumps(score)

@app.callback(Output('output-state', 'children'), Input('intermediate-value', 'children'))
def update_graph(jsonified_cleaned_data):
    # more generally, this line would be
    l = json.loads(jsonified_cleaned_data)
    #dff = pd.read_json(jsonified_cleaned_data, orient='split')
    print(l)
    return l


if __name__ == '__main__':
    app.run_server(debug=True)
