import pandas as pd
from datetime import datetime

def get_enddate(category, reqid, con):
    df = pd.read_sql("SELECT * FROM tellor_datatable where id ={} and oracle == '{}'".format(reqid, category), con)
    end_date = max(list(df['timestamp']))
    return datetime.fromisoformat(end_date)

def time_convert(raw_time):
    return datetime.utcfromtimestamp(raw_time)


