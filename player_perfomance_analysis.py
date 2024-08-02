#importing libraries 
import dash
from dash import dcc
from dash import html

import plotly.graph_objs as pgo
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State

stats=pd.read_csv("CSGO Player Dataset(FE).csv")
stats=stats.drop('Unnamed: 0',axis=1)
#names of players to be displayed on x axis
player_names=list(stats["Name"])
#stats of players to be displayed on y axis 
player_stats=list(stats.columns)

app=dash.Dash()

    
    
app.layout=html.Div([
    
    				html.H1('Player performance comparision dashboard',style={'margin-top':'40px'}),
    
    				html.Div([html.Div([html.H2('Enter the names of players:',style={'paddingRight':'30px','marginLeft':'25px'})]),
    				#this dropdown wil let you choose multiple players name at a time 
                    html.Div([dcc.Dropdown(id='names',
                                        options=[{'label': player, 'value': player} for player in player_names],
                                        value=player_names[0],
                                        multi=True)],style={'verticalAlign':'top','width':'400px','marginLeft':'25px','box-sizing': 'border-box'})],style={'display':'inline-block'}),
    
  
           
           html.Div([html.Div([html.H2("Select the stat :")],style={'paddingRight':'40px','marginLeft':'25px'}),
         #this dropdown will let you choose the stats on which you want to compare the players you already choosen from pevious dropdown            
   		html.Div([dcc.Dropdown(
        id="stats",
        options=[{'label': player, 'value': player} for player in player_stats],
        value=player_stats[0],
        clearable=False
    )],style={'width':'270px','marginLeft':'25px','box-sizing': 'border-box'})],style={'display':'inline-block','marginLeft':'70px'}),
  #upon clicking this submit button bar graph will be ploted 
  html.Div([html.Button(
        id='submit-button',n_clicks=0,children='Submit',style={'fontSize':24,'marginLeft':'670px','margin-top':'40px'})],style={'width':'270px','marginLeft':'25px','box-sizing': 'border-box'}), 
   
   dcc.Graph(id="graph"),
                
           
    
])


@app.callback(
    Output('graph', 'figure'), 
    [Input('submit-button', 'n_clicks')],
    [State('names','value'),
     State('stats','value')])
def compare_stats(n_clicks,x_value,y_value):
    
    trace_list = []
    for i in range(len(x_value)):
        trace = pgo.Bar(
            x=[x_value[i]],
            y=[stats.loc[stats['Name'] == x_value[i], y_value].values[0]],
            name=str(x_value[i])
        )
        trace_list.append(trace)
    data=trace_list
    layout=pgo.Layout(title="Stats Comparison ",barmode='group',xaxis=dict(title="Name of Players "),yaxis=dict(title="Basis of comparison"))
    fig=pgo.Figure(data,layout)
    return fig



if __name__=='__main__':
    app.run_server()