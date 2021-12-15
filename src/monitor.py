import datasource as ds
import helpers as h
import sqlite3
import os
from dotenv import load_dotenv
import json
from web3 import Web3

load_dotenv('.env')

filename = 'tellor.db'
con = sqlite3.connect(filename)
c = con.cursor()
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tellor_datatable' ''')

if c.fetchone()[0] == 1:
	init = False
else:
	init = True

print(init)


days_back = 60
results = []
ids = [1, 2, 10]

infura_link = os.getenv('INFURA_PROJECT_URL')
api_key = os.getenv('API_KEY')
with open('ext_data.json') as f:
    data = json.load(f)
tellor_dict = data['tellor']
chainlink_dict = data['chainlink']

def main():
    
    c, con = ds.database_connect(filename)
    w3 = ds.web3_connect(infura_link)


    #create tellor contract, grab tellor data
    print('getting tellor data')
    tellor_con = ds.create_contract(tellor_dict['address'], tellor_dict['abi'], w3)
    ds.tellor_grabdata(init, ids, days_back, tellor_con, results, con)

    #create all of chainlink's contracts, grab chainlink's data (separately)
    #1 - eth/usd
    print('getting chainlink data - eth/usd')
    cl_eth_usd = ds.create_contract(chainlink_dict['1']['address'], chainlink_dict['1']['abi'], w3)
    ds.chainlink_grabdata(init, cl_eth_usd, 1, days_back, results, con, scale = 1e8)
    #2 - btc/usd
    print('getting chainlink data - btc/usd')
    cl_btc_usd = ds.create_contract(chainlink_dict['2']['address'], chainlink_dict['2']['abi'], w3)
    ds.chainlink_grabdata(init, cl_btc_usd, 2, days_back, results, con, scale = 1e8)

    #10 - ampl/usd
    print('getting chainlink data - ampl/usd')
    cl_ampl_usd = ds.create_contract(chainlink_dict['10']['address'], chainlink_dict['10']['abi'], w3)
    ds.chainlink_grabdata(init, cl_ampl_usd, 10, days_back, results, con, scale = 1e18)

    print('getting ampleforth data')
    ds.ampl_grabdata(init, days_back, results)

    ds.fill_database(results, c, con)

    ds.tellor_additional(init, tellor_con, filename)


if __name__ == "__main__":
    main()
