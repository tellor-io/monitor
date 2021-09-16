import streamlit as st

from monitor import Monitor

network = st.selectbox(
    "Choose network",
    ("mainnet", "rinkeby", "polygon")
)

current_monitored_ids = {
    "mainnet": [1, 2, 10],
    "rinkeby": [1, 5, 6, 60],
    "polygon": [1, 5, 6, 60]
}

m = Monitor(network)

for i in current_monitored_ids[network]:
    m.add_request_id(i)

m.make_monitor_dataframe()