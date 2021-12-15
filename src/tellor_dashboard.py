import dash
from dash import dcc
from dash import html
from dash import dash_table
import plotly.express as px
import sqlite3
import pandas as pd
import json
from web3 import Web3
import datasource as ds
import time
import requests

app = dash.Dash(__name__)

# connect to database
con = sqlite3.connect('tellor.db')
c = con.cursor()

df = pd.read_sql("SELECT * FROM tellor_datatable", con)
df2 = df.sort_values(by = "timestamp")


###################################
###  DATA QUALITY SECTION (1)
###################################

################################### FIGURE 0: ETH/USD (ID:1)
fig = px.line(df2.loc[df2.id == 1], x="timestamp", y="price",
              color='oracle', template='plotly_dark', title='ETH/USD',
              color_discrete_sequence=['aquamarine', 'tomato'])

fig.update_layout(xaxis_title='date', title_x=0.5)
fig.update_layout(hovermode="x")
fig.update_traces(hovertemplate='Price: %{y:$.2f}<extra></extra>')
# fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig.update_traces(line=dict(width=1))
fig.update_layout({'legend_title_text': ''})

################################### FIGURE 1: BTC/USD (ID:2)

fig1 = px.line(df2.loc[df2.id == 2], x="timestamp", y="price",
               color="oracle", template='plotly_dark', title='BTC/USD',
               color_discrete_sequence=['aquamarine', 'tomato'])
fig1.update_layout(xaxis_title='date', title_x=0.5)
fig1.update_layout(hovermode="x")
fig1.update_traces(hovertemplate='Price: %{y:$.2f}<extra></extra>')
# fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig1.update_traces(line=dict(width=1))
fig1.update_layout({'legend_title_text': ''})

################################### FIGURE 2: AMPL/USD
# fig2 = px.line(df4, x="timestamp", y="price",template = 'plotly_dark', title = 'AMPL/USD price via Tellor')
fig2 = px.line(df2.loc[df2.id == 10], x="timestamp", y="price", template='plotly_dark', title='AMPL/USD',
               color='oracle', color_discrete_sequence=['aquamarine', 'tomato', 'mediumslateblue'])

fig2.update_layout(xaxis_title='date', title_x=0.5)
fig2.update_layout(hovermode="x")
fig2.update_traces(hovertemplate='Price: %{y:$.2f}<extra></extra>')
# fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
# fig2.update_traces(line=dict(color="aquamarine", width=1))
fig2.update_layout({'legend_title_text': ''})
fig2.update_traces(line=dict(width=1))


'''
### TABLE FOR UPDATE MONITORING
tellor_api = "http://api.tellorscan.com/prices/1"
time_gap = {"yellow": 12 * 60 * 60, "red": 24 * 60 * 60}
r = requests.get(tellor_api)
files = r.json()

important_ids = [1, 2, 5, 10, 57]
df_list = []
for file in files:
    if int(file['id']) in important_ids:
        time_update = int(file['timestamp'])
        diff = round((time.time() - time_update) / 3600, 3)
        df_list.append([file['id'], file['name'], diff])

df_tab = pd.DataFrame(df_list, columns=['id', 'price feed', 'hours since last update'])
'''
app.layout = html.Div(children=[
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='four columns div-user-controls',
                          children=[
                              html.H2('TELLOR DASHBOARD'),
                              html.P('''Visualising Tellor data with Plotly - Dash'''),
                            '''
                              dash_table.DataTable(
                                  id='table_id',
                                  columns=[{'name': i, 'id': i} for i in df_tab.columns],
                                  data=df_tab.to_dict("rows"),
                                  style_cell={'textAlign': 'center'},
                                  style_data={'color': 'mediumslategray'},
                                  style_data_conditional=[
                                      {'if': {
                                          'filter_query': '{hours since last update} >= 12 && {hours since last update} < 24',
                                          'column_id': 'hours since last update'
                                          },
                                       'backgroundColor': 'yellow',
                                       'color': 'white'
                                       },
                                      {'if': {'filter_query': '{hours since last update} < 12',
                                              'column_id': 'hours since last update'
                                              },
                                       'backgroundColor': 'mediumspringgreen',
                                       'color': 'white'
                                       },
                                      {'if': {'filter_query': '{hours since last update} >= 24',
                                              'column_id': 'hours since last update'
                                              },
                                       'backgroundColor': 'tomato',
                                       'color': 'white'
                                       }
                                  ]
                              ) '''

                          ]),  # Define the left element
                 html.Div(className='eight columns div-for-charts bg-grey',
                          children=[
                              dcc.Graph(
                                  id='tellor ETH/USD',
                                  figure=fig
                              ),
                              dcc.Graph(
                                  id='tellor BTC/USD',
                                  figure=fig1
                              ),
                              dcc.Graph(
                                  id='tellor AMPL/USD',
                                  figure=fig2
                              )
                          ])
             ])
])

if __name__ == '__main__':
    app.run_server(debug=True)