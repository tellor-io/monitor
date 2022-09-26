import datasource as ds
import helpers as h
import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import pandas as pd
import json
from web3 import Web3

load_dotenv('../.env')

DATABASE_URL = os.getenv('DATABASE_URL')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DUNE_USERNAME = os.getenv('DUNE_USERNAME')
DUNE_PASSWORD = os.getenv('DUNE_PASSWORD')

DUNE_QUERY_ID = os.getenv('DUNE_QUERY_ID')

dune_login = (DUNE_USERNAME, DUNE_PASSWORD)

# con = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASSWORD, host = DB_HOST)
# c = con.cursor()

"""
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tellor_datatable' ''')

if c.fetchone()[0] == 1:
	init = False
else:
	init = True

DUNE_USERNAME = os.getenv('DUNE_USERNAME')
DUNE_PASSWORD = os.getenv('DUNE_PASSWORD')
DUNE_QUERY_ID = int(os.getenv('DUNE_QUERY_ID'))

dune_login = (DUNE_USERNAME, DUNE_PASSWORD)

print(init)
"""
init = False

days_back = 124
results = []
ids = [1, 2, 10]

infura_link = os.getenv('INFURA_PROJECT_URL')
with open('../data/ext_data.json') as f:
    data = json.load(f)
tellor_dict = data['tellor']
chainlink_dict = data['chainlink']


def main():
    c, con = ds.database_connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    w3 = ds.web3_connect(infura_link)

    # create tellor contract, grab tellor data
    print('getting tellor data')
    tellor_con = ds.create_contract(tellor_dict['address'], tellor_dict['abi'], w3)
    ds.tellor_grabdata(init, ids, days_back, tellor_con, results, con)

    # create all of chainlink's contracts, grab chainlink's data (separately)
    # 1 - eth/usd
    print('getting chainlink data - eth/usd')
    cl_eth_usd = ds.create_contract(chainlink_dict['1']['address'], chainlink_dict['1']['abi'], w3)
    ds.chainlink_grabdata(init, cl_eth_usd, 1, days_back, results, con, scale=1e8)
    # 2 - btc/usd
    print('getting chainlink data - btc/usd')
    cl_btc_usd = ds.create_contract(chainlink_dict['2']['address'], chainlink_dict['2']['abi'], w3)
    ds.chainlink_grabdata(init, cl_btc_usd, 2, days_back, results, con, scale=1e8)

    # 10 - ampl/usd
    print('getting chainlink data - ampl/usd')
    cl_ampl_usd = ds.create_contract(chainlink_dict['10']['address'], chainlink_dict['10']['abi'], w3)
    ds.chainlink_grabdata(init, cl_ampl_usd, 10, days_back, results, con, scale=1e18)

    print('getting ampleforth data')
    ds.ampl_grabdata(init, days_back, results, con)

    print('getting makerDAO data from dune analytics')
    try:
        ds.makerdao_grabdata(init, results, dune_login, id=int(DUNE_QUERY_ID))
    except:
        print("unable to get makerdao data from dune")

    ds.fill_database(results, c, con)


if __name__ == "__main__":
    main()
