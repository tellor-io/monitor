import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd


app = dash.Dash(__name__)


#connect to db
import sqlite3
from web3 import Web3
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dateutil import parser

#connect to database
con = sqlite3.connect('tellor_dashboard_v0.db')
c = con.cursor()

df = pd.read_sql("SELECT * FROM tellor_table_2", con)

df2 = df.sort_values(by="timestamp")

###################################
### TELLOR DATA SECTION (1)
###################################

################################### FIGURE 0: ETH/USD
fig = px.line(df2.loc[df2.id == 1], x="timestamp", y="price",
                  color = 'category' , template = 'plotly_dark', title = 'ETH/USD',
                  color_discrete_sequence = ['aquamarine', 'tomato'])

fig.update_layout(xaxis_title = 'date', title_x = 0.5)
fig.update_layout(hovermode="x")
fig.update_traces(hovertemplate = 'Price: %{y:$.2f}<extra></extra>')
#fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig.update_traces(line=dict(width=1))
fig.update_layout({'legend_title_text': ''})

################################### FIGURE 01: BTC/USD
fig1 = px.line(df2.loc[df2.id == 2], x="timestamp", y="price",
                  color="category", template = 'plotly_dark', title = 'BTC/USD')
fig1.update_layout(xaxis_title = 'date', title_x = 0.5)
fig1.update_layout(hovermode="x")
fig1.update_traces(hovertemplate = 'Price: %{y:$.2f}<extra></extra>')
#fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig1.update_traces(line=dict(color="aquamarine", width=1))
fig1.update_layout({'legend_title_text': ''})

################################### FIGURE 0: AMPL/USD




#fig2 = px.line(df4, x="timestamp", y="price",template = 'plotly_dark', title = 'AMPL/USD price via Tellor')
fig2 = px.line(df2.loc[df2.id == 10], x="timestamp", y="price",template = 'plotly_dark', title = 'AMPL/USD', color = 'category', color_discrete_sequence = ['tomato','aquamarine', 'mediumslateblue'])
fig2.update_layout(xaxis_title = 'date', title_x = 0.5)
fig2.update_layout(hovermode="x")
fig2.update_traces(hovertemplate = 'Price: %{y:$.2f}<extra></extra>')
#fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
#fig2.update_traces(line=dict(color="aquamarine", width=1))
fig2.update_layout({'legend_title_text': ''})
fig2.update_traces(line=dict(width=1))




app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls',
                                  children = [
                                    html.H2('TELLOR DASHBOARD'),
                                    html.P('''Visualising Tellor data with Plotly - Dash'''),
                                    html.P('''Pick a visualization option from the dropdown below.''') 

                                ]),  # Define the left element
                                  html.Div(className='eight columns div-for-charts bg-grey',
                                  children = [
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