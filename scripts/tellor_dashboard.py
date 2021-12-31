import dash
from dash import dcc
from dash import html
from dash import dash_table
from datetime import datetime
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

app = dash.Dash(__name__)
server = app.server

load_dotenv('../.env')


engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    host = os.getenv('DB_HOST'),
    port = 5432,
    database = os.getenv('DB_NAME'),
)

engine = create_engine(engine_string)
df = pd.read_sql_table('test',engine)
df2 = df.sort_values(by = "time")

###################################
###  DATA QUALITY SECTION (1)
###################################

################################### FIGURE 0: ETH/USD (ID:1)
fig = px.line(df2.loc[df2.id == 1], x="time", y="price",
              color='oracle', template='plotly', title='ETH/USD',
              color_discrete_sequence=['#3fd491', '#233047'])

fig.update_layout(xaxis_title='date', title_x=0.5)
fig.update_layout(hovermode="x")
fig.update_traces(hovertemplate='Price: %{y:$.2f}<extra></extra>')
fig.update_layout({'legend_title_text': ''})
fig.update_layout(font_family="Inconsolata")
fig.update_layout(font_color='#535959')
fig.update_traces(line=dict(width=2))
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1d",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="1w",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
)

################################### FIGURE 1: BTC/USD (ID:2)

fig1 = px.line(df2.loc[df2.id == 2], x="time", y="price",
               color="oracle", template='plotly', title='BTC/USD',
               color_discrete_sequence=['#3fd491', '#233047'])
fig1.update_layout(xaxis_title='date', title_x=0.5)
fig1.update_layout(hovermode="x")
fig1.update_traces(hovertemplate='Price: %{y:$.2f}<extra></extra>')
# fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig1.update_traces(line=dict(width=2))
fig1.update_layout({'legend_title_text': ''})
fig1.update_layout(font_family="Inconsolata")
fig1.update_layout(font_color='#535959')
fig1.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1d",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="1w",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
)

################################### FIGURE 2: AMPL/USD
# fig2 = px.line(df4, x="timestamp", y="price",template = 'plotly_dark', title = 'AMPL/USD price via Tellor')
fig2 = px.line(df2.loc[df2.id == 10], x="time", y="price", template='plotly', title='AMPL/USD',
               color='oracle', color_discrete_sequence=['#3fd491', '#233047', 'mediumslateblue'])

fig2.update_layout(xaxis_title='date', title_x=0.5)
fig2.update_layout(hovermode="x")
fig2.update_traces(hovertemplate='Price: %{y:$.2f}<extra></extra>')
fig2.update_layout({'legend_title_text': ''})
fig2.update_traces(line=dict(width=2))
fig2.update_layout(font_color='#535959')
fig2.update_layout(font_family="Inconsolata")
fig2.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1d",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="1w",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
)

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

important_ids = [1, 2, 10]
#timestamp, price, id, oracle)
table = []
df_tel = df2[df2['oracle'] == 'tellor']

for id in important_ids:
    df_sub = df_tel[df_tel['id']== id]['time'].max()
    change = (datetime.now() - datetime.fromisoformat(df_sub)).total_seconds() / 3600
    table.append([id, change])

df_tab = pd.DataFrame(table, columns = ['id', 'hours since last update'])


app.layout = html.Div(children=[
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='four columns div-user-controls',
                          children=[
                              html.H2('tellor dashboard'),
                              html.P('''visualising tellor data with plotly - dash'''),

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
                                       'backgroundColor': '#5a5c5c',
                                       'color': 'white'
                                       },
                                      {'if': {'filter_query': '{hours since last update} < 12',
                                              'column_id': 'hours since last update'
                                              },
                                       'backgroundColor': '#3fd491',
                                       'color': 'white'
                                       },
                                      {'if': {'filter_query': '{hours since last update} >= 24',
                                              'column_id': 'hours since last update'
                                              },
                                       'backgroundColor': '#1a1a1a',
                                       'color': 'white'
                                       }
                                  ]
                              )

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
    #server = app.server
    app.run_server(debug=True)