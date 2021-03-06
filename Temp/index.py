import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2
from apps import BetterDash


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/Home':
        return app1.layout
    elif pathname == '/Main':
        return BetterDash.layout
    else:
        return app1.layout

if __name__ == '__main__':
    app.run_server(debug=True)
