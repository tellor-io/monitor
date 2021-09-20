import streamlit as st

from monitor import Monitor

current_monitored_ids = {
    "mainnet": [1, 2, 10],
    "polygon": [1, 5, 6, 60]
}

m = Monitor(current_monitored_ids)


m.make_monitor_dataframe()

st.write("For mapping of requestId numbers to asset tickers, refer to this [gsheet](https://docs.google.com/spreadsheets/d/1BK7Cs0K2W-bRaNpuvzFbVX50CgjXH7k-HKAuuWxTiW8/edit?usp=sharing)")