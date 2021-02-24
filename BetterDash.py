# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import os
import base64
import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

tweets_path = 'RealTweets/'

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(tweets_path) if isfile(join(tweets_path, f))]

IMAGES = onlyfiles

app.layout = html.Div([
    html.Img(id='tweet'),

    html.Button('Real', id='btn-nclicks-1', n_clicks=0),
    html.Button('Fake Bad', id='btn-nclicks-2', n_clicks=0),
    html.Button('Fake Good/Funny', id='btn-nclicks-3', n_clicks=0),
    html.Button('Fake ok but fix end', id='btn-nclicks-4', n_clicks=0),

    html.Div(id='container-button-timestamp')
])

@app.callback(Output('container-button-timestamp', 'children'),
              Output('tweet', 'src'),
              Input('btn-nclicks-1', 'n_clicks'),
              Input('btn-nclicks-2', 'n_clicks'),
              Input('btn-nclicks-3', 'n_clicks'),
              Input('btn-nclicks-4', 'n_clicks'))
def displayClick(btn1, btn2, btn3, btn4):

    imgs = IMAGES.copy()
    if btn1+btn2 % len(imgs) == 0:
        random.shuffle(imgs)
     #tweet or faketweet
    print(btn1+btn2)
    print(imgs[(btn1+btn2)%len(imgs)])


    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        print('clicked Real')
        if imgs[(btn1+btn2)%len(imgs)][0] == 't':
            msg = 'Correct'
        else:
            msg = "WRONG"

    elif 'btn-nclicks-3' in changed_id:
        print('clicked Fake')
        if imgs[(btn1+btn2)%len(imgs)][0] == 'f':
            msg = 'Correct'
        else:
            msg = "WRONG"
    else:
        msg = 'None of the buttons have been clicked yet'

    image_path = tweets_path + str(imgs[(btn1+btn2+1)%len(imgs)])
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    out = 'data:image/png;base64,{}'.format(encoded_image.decode())

    return html.Div(msg), out

if __name__ == '__main__':
    app.run_server(debug=True)
