#goal: create main data grabbing funcs (invlude boolean flag for init)
import sqlite3
from web3 import Web3
from datetime import datetime, timedelta
import requests
import pandas as pd
import helpers
import math
from duneanalytics import DuneAnalytics
import os

#database
def database_connect(filename):
    con = sqlite3.connect(filename)
    c = con.cursor()
    c.execute(''' CREATE TABLE if not exists tellor_datatable (timestamp, price, id, oracle)''')
    con.commit()
    return (c, con)

#connect to web3
def web3_connect(infura_url):
    w3 = Web3(Web3.HTTPProvider(infura_url))
    return w3

def create_contract(add, abi, w3):
    return w3.eth.contract(address = add, abi = abi)


def tellor_additional(init, contract, filename):

    con = sqlite3.connect(filename)
    c = con.cursor()
    if init:
        c.execute(''' CREATE TABLE if not exists tellor_additional (time, disputes, stakers)''')

    time = datetime.now()
    dispute_count = contract.functions.disputeCount().call()
    #stakers = contract.functions.stakeCount().call()
    stakers = 0
    result = [(time, dispute_count, stakers)]

    c.executemany("insert into tellor_additional values(?, ?, ?)", result)

    con.commit()
    con.close()


#tellor
def tellor_grabdata(init, ids, days_back, contract, results, con):
    scale = 1e6
    for id in ids:
        tellor_data = contract.functions.getCurrentValue(id).call()
        timestamp = datetime.fromtimestamp(int(tellor_data[2]))
        if id == 10:
            price = tellor_data[1] / 1e18

        else:
            price = tellor_data[1] / scale

        results.append((timestamp, price, id, 'tellor'))

        if init:
            old_date = (datetime.now() - timedelta(days = days_back))
        else:
            old_date = helpers.get_enddate('tellor', id, con)

        while old_date < datetime.fromtimestamp(tellor_data[2]):
            tellor_data = contract.functions.getDataBefore(id, tellor_data[2]).call()
            timestamp = datetime.fromtimestamp(int(tellor_data[2]))
            price = tellor_data[1] / scale
            if id == 10:
                #if timestamp.hour == 0:
                results.append((timestamp, price / 1e12, id, 'tellor'))

            else:
                results.append((timestamp, price, id, 'tellor'))



#chainlink
def chainlink_grabdata(init, contract, id, days_back, results, con, scale = 1, inverse = False):
    latest_data = contract.functions.latestRoundData().call()
    if init:
        old_date = datetime.now() - timedelta(days = days_back)
    else:
        old_date = helpers.get_enddate('chainlink', id, con)

    if inverse:
        price = 1 / (latest_data[1] / scale)
    else:
        price = latest_data[1] / scale
    results.append((helpers.time_convert(latest_data[3]), price, id, "chainlink"))

    curr_round_id = latest_data[0]
    curr_date = latest_data[3]

    while datetime.fromtimestamp(curr_date) > old_date:
        curr_round_id = curr_round_id - 1
        past_data = contract.functions.getRoundData(curr_round_id).call()
        curr_date = past_data[3]

        if inverse:
            price = 1 / (past_data[1] / scale)
        else:
            price = past_data[1] / scale

        results.append((helpers.time_convert(past_data[3]), price, id, "chainlink"))

#ampleforth
def ampl_grabdata(init, days_back, results, con):
    ampl_url = 'https://web-api.ampleforth.org/eth/oracle-history'

    r = requests.get(ampl_url)
    files = r.json()
    ampl_dict = files["rateOracleProviderHistory"]["reports"]["ampleforth.org"]

    ampl_df = pd.DataFrame(ampl_dict)
    payload = list(ampl_df['payload'])
    timestamps = list(ampl_df['timestampSec'])
    new_timestamps = [datetime.fromtimestamp(i) for i in timestamps]

    if init:
        old_date = datetime.now() - timedelta(days = days_back)
    else:
        old_date = helpers.get_enddate('ampleforth', 10, con)

    for i in range(0, len(new_timestamps)):
        if new_timestamps[i] > old_date:
            results.append((new_timestamps[i], payload[i], 10, 'ampleforth'))


### NOT AUTOMATIC YET
def makerdao_grabdata(init, results, login, id):
    dune = DuneAnalytics(login[0], login[1])
    dune.login()
    dune.fetch_auth_token()
    result_id = dune.query_result_id(query_id = id)
    data = dune.query_result(result_id)
    data2 = data['data']['get_result_by_result_id']

    times = []
    values = []

    for datum in data2:
        time = datetime.fromisoformat(datum['data']['evt_block_time'])
        time = time.replace(tzinfo = None)
        hexstr = "0" + datum['data']['val'].replace("\\", "")
        val = Web3.toInt(hexstr = hexstr) / 1e18
        #check for digits - why is this being weird?
        digits = int(math.log10(val)) + 1

        if digits == 4:
            times.append(time)
            values.append(val)

    if len(times) == 0 or len(values) == 0:
        print("no makerDAO data retrieved")
    
    else:
        results.append((times[0], values[0], 1, 'makerDAO'))

        for i in range(1, len(values)):
            if values[i] != values[i - 1]:
                results.append((times[i], values[i], 1, 'makerDAO'))

def fill_database(results, c, con):
    c.executemany("insert into tellor_datatable values(?, ?, ?, ?)", results)
    con.commit()
    con.close()