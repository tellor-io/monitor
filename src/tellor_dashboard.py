import time

import dash
from dash import dcc
from dash import html
from dash import dash_table
from datetime import datetime
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import os
import requests
import time
from dotenv import load_dotenv

from src import eth_usd, btc_usd, ampl_uspce

app = dash.Dash(__name__)
server = app.server

load_dotenv(".env")


engine_string = (
    "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=5432,
        database=os.getenv("DB_NAME"),
    )
)

engine = create_engine(engine_string, isolation_level="READ UNCOMMITTED")
df = pd.read_sql_table("t360", engine)
df2 = df.sort_values(by="time")

###################################
###  DATA QUALITY SECTION (1)
###################################

################################### FIGURE 0: ETH/USD (ID:1)
fig = px.line(
    df2.loc[df2.id == eth_usd],
    x="time",
    y="price",
    color="oracle",
    template="plotly",
    title="ETH/USD",
    color_discrete_sequence=["#898f8c", "#3fd491", "#233047"],
)

fig.update_layout(xaxis_title="date", title_x=0.5)
fig.update_layout(hovermode="x")
fig.update_traces(hovertemplate="Price: %{y:$.2f}<extra></extra>")
fig.update_layout({"legend_title_text": ""})
fig.update_layout(font_family="Inconsolata")
fig.update_layout(font_color="#535959")
fig.update_traces(line=dict(width=2))
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        rangeslider=dict(visible=False),
        type="date",
    )
)

################################### FIGURE 1: BTC/USD (ID:2)

fig1 = px.line(
    df2.loc[df2.id == btc_usd],
    x="time",
    y="price",
    color="oracle",
    template="plotly",
    title="BTC/USD",
    color_discrete_sequence=["#3fd491", "#233047"],
)
fig1.update_layout(xaxis_title="date", title_x=0.5)
fig1.update_layout(hovermode="x")
fig1.update_traces(hovertemplate="Price: %{y:$.2f}<extra></extra>")
# fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig1.update_traces(line=dict(width=2))
fig1.update_layout({"legend_title_text": ""})
fig1.update_layout(font_family="Inconsolata")
fig1.update_layout(font_color="#535959")
fig1.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        rangeslider=dict(visible=False),
        type="date",
    )
)

################################### FIGURE 2: AMPL/USD
# fig2 = px.line(df4, x="timestamp", y="price",template = 'plotly_dark', title = 'AMPL/USD price via Tellor')
fig2 = px.line(
    df2.loc[df2.id == ampl_uspce],
    x="time",
    y="price",
    template="plotly",
    title="AMPL/USD",
    color="oracle",
    color_discrete_sequence=["#3fd491", "#233047", "mediumslateblue"],
)

fig2.update_layout(xaxis_title="date", title_x=0.5)
fig2.update_layout(hovermode="x")
fig2.update_traces(hovertemplate="Price: %{y:$.2f}<extra></extra>")
fig2.update_layout({"legend_title_text": ""})
fig2.update_traces(line=dict(width=2))
fig2.update_layout(font_color="#535959")
fig2.update_layout(font_family="Inconsolata")
fig2.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        rangeslider=dict(visible=False),
        type="date",
    )
)


### TABLE FOR UPDATE MONITORING
tellor_api = "http://api.tellorscan.com/mainnet/price/"
id_ethusd = "0x83a7f3d48786ac2667503a61e8c415438ed2922eb86a2906e4ee66d9a2ce4992"
id_btcusd = "0xa6f013ee236804827b77696d350e9f0ac3e879328f2a3021d473a0b778ad78ac"
id_amplusd = "0x0d12ad49193163bbbeff4e6db8294ced23ff8605359fd666799d4e25a3aa0e3a"
id_trbusd = "0x5c13cd9c97dbb98f2429c101a2a8150e6c7a0ddaff6124ee176a3a411067ded0"
id_uspce = "0x612ec1d9cee860bb87deb6370ed0ae43345c9302c085c1dfc4c207cbec2970d7"
relevant_ids = [id_ethusd, id_btcusd, id_amplusd, id_uspce, id_trbusd]

dataspecs = {
    id_ethusd: "ETH/USD",
    id_btcusd: "BTC/USD",
    id_amplusd: "AMPL/USD",
    id_uspce: "USPCE",
    id_trbusd: "TRB/USD",
}

try:
    df_list = []
    for qid in relevant_ids:
        full_url = tellor_api + qid
        r = requests.get(full_url)
        most_recent_price_info = r.json()[0]
        print(most_recent_price_info)
        diff = round((time.time() - int(most_recent_price_info["timestamp"])) / 3600, 3)
        if qid == id_amplusd or qid == id_uspce:
            most_recent_price_info["value"] = most_recent_price_info["value"] / 1e12
        df_list.append(
            [dataspecs[qid], round(most_recent_price_info["value"], 2), diff]
        )

    df_tab = pd.DataFrame(
        df_list, columns=["price feed", "current price", "hours since last update"]
    )

except requests.exceptions.JSONDecodeError:
    print("unable to grab price data of selected feeds")
    df_tab = pd.DataFrame(
        [], columns=["price feed", "current price", "hours since last update"]
    )


try:
    url = "https://api.tellorscan.com/mainnet/info"
    r2 = requests.get(url)
    files2 = r2.json()
    df_list2 = [[files2["stakerCount"], files2["disputeCount"]]]
    df_tab2 = pd.DataFrame(
        df_list2, columns=["number of stakers", "number of disputes"]
    )

except requests.exceptions.JSONDecodeError:
    print("unable to retrieve mainnet info data")
    df_tab2 = pd.DataFrame([], columns=["number of stakers", "number of disputes"])


app.layout = html.Div(
    children=[
        html.Div(
            className="row",  # Define the row element
            children=[
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H1("tellor dashboard"),
                        html.P("""visualizing tellor data with plotly - dash"""),
                        html.Br(),
                        dash_table.DataTable(
                            id="table_id",
                            columns=[{"name": i, "id": i} for i in df_tab.columns],
                            data=df_tab.to_dict("records"),
                            style_cell={"textAlign": "center"},
                            style_data={"color": "mediumslategray"},
                            style_data_conditional=[
                                {
                                    "if": {
                                        "filter_query": "{hours since last update} >= 12 && {hours since last update} < 24",
                                        "column_id": "hours since last update",
                                    },
                                    "backgroundColor": "#5a5c5c",
                                    "color": "white",
                                },
                                {
                                    "if": {
                                        "filter_query": "{hours since last update} < 12",
                                        "column_id": "hours since last update",
                                    },
                                    "backgroundColor": "#3fd491",
                                    "color": "white",
                                },
                                {
                                    "if": {
                                        "filter_query": "{hours since last update} >= 24",
                                        "column_id": "hours since last update",
                                    },
                                    "backgroundColor": "#1a1a1a",
                                    "color": "white",
                                },
                            ],
                        ),
                        html.Br(),
                        dash_table.DataTable(
                            id="table2_id",
                            columns=[{"name": i, "id": i} for i in df_tab2.columns],
                            data=df_tab2.to_dict("records"),
                            style_cell={"textAlign": "center"},
                            style_data={"color": "mediumslategray"},
                        ),
                    ],
                ),  # Define the left element
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="tellor ETH/USD", figure=fig),
                        dcc.Graph(id="tellor AMPL/USD", figure=fig2),
                        dcc.Graph(id="tellor BTC/USD", figure=fig1),
                    ],
                ),
            ],
        )
    ]
)

if __name__ == "__main__":
    # server = app.server
    app.run_server(debug=True)
