import json

import dash
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button('Button 1', id='btn-1'),
    html.Button('Button 2', id='btn-2'),
    html.Button('Button 3', id='btn-3'),
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div(id='container')
])






@app.callback(Output('intermediate-value', 'children'),
              Input('btn-1', 'n_clicks'),
              Input('btn-2', 'n_clicks'),
              Input('btn-3', 'n_clicks'))
def display(btn1, btn2, btn3):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    ctx_msg = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)

    score = [ctx.inputs]
    print(ctx.triggered)
    return json.dumps(score)




@app.callback(Output('container', 'children'), Input('intermediate-value', 'children'))
def update_graph(jsonified_cleaned_data):
    # more generally, this line would be
    l = json.loads(jsonified_cleaned_data)
    #dff = pd.read_json(jsonified_cleaned_data, orient='split')
    print(l)
    return html.Div([
        html.Table([
            html.Tr([html.Th('Button 1'),
                     html.Th('Button 2'),
                     html.Th('Button 3'),
                     html.Th('Most Recent Click')]),
            html.Tr([html.Td(l[0]['btn-1.n_clicks'] or 0),
                     html.Td(l[0]['btn-2.n_clicks'] or 0),
                     html.Td(l[0]['btn-3.n_clicks'] or 0)])
        ]),
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
