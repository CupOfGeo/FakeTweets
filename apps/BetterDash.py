# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import os
import base64
import random
import json
import random


from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
import psycopg2

import numpy as np
import pandas as pd
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap

df = pd.read_csv('all_tweets.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from app import app
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server
# app.title='FAKENEWS'

layout = html.Div([
    html.Title("HELLO", id='tit'),
    dcc.Graph(id='score_map'),
    html.Img(id='tweet'),


    html.Button('Real', id='btn-nclicks-1', n_clicks=0),
    html.Button('Fake Good/Funny', id='btn-nclicks-3', n_clicks=0),
    html.Button('Fake Bad', id='btn-nclicks-2', n_clicks=0),
    html.Button('Fake ok but fix end', id='btn-nclicks-4', n_clicks=0),

    html.Div(id='container-button-timestamp'),

    dcc.Store(id='idx', storage_type='session'),
    dcc.Store(id='local', storage_type='session')
    #Output('intermediate-value', 'children')

])

@app.callback(Output('score_map','figure'),
                Input('local', 'modified_timestamp'),
                State('local', 'data'))
def displayScore(ts, score):
    if ts is None:
        raise PreventUpdate

    score = score or [0,0,0,0]
    val = [[score[0],score[1]],[score[3],score[2]]]
    #score is confusion matrix
    #score[0] is real tweets you said were real
    #score[1] is number of real tweets you said were fake
    #score[2] is fake tweets you said were fake
    #score[3] is number of fake tweets you said were real



    #print(score)

    fig = px.imshow(val,
                labels=dict(x="Actual", y="Your Guess"),
                x=['Real', 'Fake'],
                y=['Real', 'Fake']
               )
    fig.update_xaxes(side="top")

    return fig


@app.callback(Output('tweet', 'src'),Output('idx', 'data'),Input('local', 'data'),State('idx', 'data'))
def displayTweet(s,rand_idx):

    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    #print('CTX:',trigger_id, rand_idx,s)

    rand_ind = random.randint(0, len(df))

    cur = df.iloc[rand_ind]
    text = cur.Tweet#.iloc[idx_list[0]]
    # print(text)
    # print(cur.temp)
    # print(rand_ind)
    text = "\n".join(textwrap.wrap(text, width=39))
    img_text = Image.new('RGB', (480, 28*len(text.split('\n'))), (255,255,255))
    d = ImageDraw.Draw(img_text)
    font = ImageFont.truetype(r'Tweet_template/EncodeSansSemiExpanded-Regular.ttf', 22)

    d.text((17, 0), text, font=font, fill=(0, 0, 0))
    #img_text.save( 'img_text.jpg' )
    img_text

    list_im = ['Tweet_template/img_top.jpg', 'Tweet_template/img_bot.jpg']
    imgs    = [ PIL.Image.open(i) for i in list_im ]
    imgs.insert(1,img_text)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.vstack(imgs)
    imgs_comb = PIL.Image.fromarray(imgs_comb)
    return imgs_comb, rand_ind




@app.callback(Output('local', 'data'),
            Output('container-button-timestamp', 'children'),
              Input('idx','data'),
              Input('btn-nclicks-1', 'n_clicks'),
              Input('btn-nclicks-2', 'n_clicks'),
              Input('btn-nclicks-3', 'n_clicks'),
              Input('btn-nclicks-4', 'n_clicks'),
              State('local', 'data'))
def displayClick(rand_ind,btn1, btn2, btn3, btn4, score):
    if btn1 is None or btn2 is None or btn3 is None or btn4 is None:
        raise PreventUpdate
    #print('FUCKKKSKKSKSKSKSK', rand_ind)


            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #print(dash.callback_context.triggered)




    #DATABASE
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'))
        cur = conn.cursor()
    except:
        print("I am unable to connect to the database")



    #score is confusion matrix
    #score[0] is real tweets you said were real
    #score[1] is number of real tweets you said were fake
    #score[2] is fake tweets you said were fake
    #score[3] is number of fake tweets you said were real
    score = score or [0,0,0,0]




    if 'btn-nclicks-1' in changed_id:
        try:
            cur.execute("INSERT INTO test (num, data) VALUES (1, '{}')".format(rand_ind))
        except:
            print("droped button 1")

        if df.temp.iloc[rand_ind] == 0:
            msg = 'Correct that was real'
            score[0] += 1
        else:
            msg = "Wrong that was fake"
            score[1] += 1

    elif 'btn-nclicks-2' in changed_id:
        try:
            cur.execute("INSERT INTO test (num, data) VALUES (2,'{}')".format(rand_ind))
        except:
            print("droped button 2")

        if df.temp.iloc[rand_ind] == 0:
            msg = "Wrong that was a Real tweet"
            score[3] += 1

        else:
            msg = "Correct that was a Fake tweet"
            score[2] += 1



    elif 'btn-nclicks-3' in changed_id:
        try:
            cur.execute("INSERT INTO test (num, data) VALUES (3,'{}')".format(rand_ind))
        except:
            print("droped button 3")

        if df.temp.iloc[rand_ind] != 0:
            msg = 'Correct that was fake'
            score[2] += 1
        else:
            msg = "Wrong that was real"
            score[3] += 1

    elif 'btn-nclicks-4' in changed_id:
        try:
            cur.execute("INSERT INTO test (num, data) VALUES (4, '{}')".format(rand_ind))
        except:
            print("droped button 4")

        if df.temp.iloc[rand_ind] != 0:
            msg = 'Correct that was fake. Thanks will look into that'
            score[2] += 1
        else:
            msg = "Wrong that was real hes just bad"
            score[3] += 1

    #elif 'btn-nclicks-5' in changed_id: TODO add back button
    # image_path = tweets_path + str(imgs[(btn1+btn2-1)%len(imgs)])
    else:
        msg = 'None of the buttons have been clicked yet'
        #raise PreventUpdate

    try:
        conn.commit() # <--- makes sure the change is shown in the database
        cur.close()
        conn.close()
    except:
        pass

    print(msg)

    return score,html.Div(msg)

# if __name__ == '__main__':
#     app.run_server(debug=True)
