# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 10:08:47 2021

@author: Declan
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table
def generate_table(dataframe, max_rows=35):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)

df = pd.read_csv('/users/declan/desktop/BruinsPlayerStats.csv')
html.Label('Select Stat'),


fig2 = px.bar(df, x="name", y=['gamesPlayed', 'points', 'goals', 'assists', 'primaryAssists', 'secondaryAssists', 'shotsOnGoal', 'penalties', 'penaltyMinutes', 'hits', 'shotsBlocked'], title='Filter the bar chart by clicking on the skater stats')
fig2.show()

app.layout = html.Div([
    html.H1('Boston Bruins Skater Stats for the 2019-2020 Season',
            style={'textAlign' : 'center'}),
    html.A([html.Img(
                src='/users/declan/desktop/BOS.png')],
           href='https://www.nhl.com/bruins',
           target='_blank'),
    html.H6('Click on the image to go to the official website of the Boston Bruins'),
    dcc.Graph(figure=fig2, id='stat_plot'),
    dcc.Dropdown(id='dropdown', options=[{'label': i, 'value': i} for i in df.name.unique()], multi=True, placeholder='Filter by player...'),
    html.Div(id='players'),
    html.Div([html.H4('Choose what positions you would like to see:'),
              dcc.Checklist(
                  options=[{'label': 'LW', 'value': 'LW'},
                           {'label': 'C', 'value': 'C'},
                           {'label': 'RW', 'value': 'RW'},
                           {'label': 'D', 'value': 'D'}],
                  value=['LW', 'D'],
                  id = 'position_checklist')],
            style={'width':'49%', 'float' : 'right'}),
   html.Div(id='table_div'),
   ])
    

    
@app.callback(
    Output(component_id="table_div", component_property="children"),
    [Input(component_id="position_checklist", component_property="value")]
)
def update_table(positions):
    x = df[df.position.isin(positions)].sort_values('gamesPlayed', ascending=False)
    return generate_table(x)


@app.callback(
    Output(component_id="stat_plot", component_property="figure"),
    [Input(component_id="position_checklist", component_property="value")]
)
def update_plot(positions):
    fig2 = px.bar(df, x="name", y=['gamesPlayed', 'points', 'goals', 'assists', 'primaryAssists', 'secondaryAssists', 'shotsOnGoal', 'penalties', 'penaltyMinutes', 'hits', 'shotsBlocked'], title='Filter the bar chart by clicking on the skater stats')
    return fig2

@app.callback(
    dash.dependencies.Output('players', 'children'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def player_display(players):
    if players is None:
        return generate_table(df)
    
    dff = df[df.name.str.contains('|'.join(players))]
    return generate_table(dff)


if __name__ == '__main__':
    app.run_server(debug=False)