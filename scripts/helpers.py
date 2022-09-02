import pandas as pd
from datetime import datetime
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv('../.env')

def get_enddate(oracle, reqid):
    engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=5432,
        database=os.getenv('DB_NAME'),
    )

    engine = create_engine(engine_string)
    df = pd.read_sql_table('test', engine)
    df_source = df[df['oracle'] == oracle]
    df_sub = df_source[df_source['id'] == reqid]['time'].max()

    end_date = datetime.fromisoformat(df_sub)

    #df = pd.read_sql("SELECT * FROM tellor_datatable where id ={} and oracle == '{}'".format(reqid, category), con)
    #end_date = max(list(df['timestamp']))
    return end_date

def time_convert(raw_time):
    return datetime.utcfromtimestamp(raw_time)


