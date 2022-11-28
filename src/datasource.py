#goal: create main data grabbing funcs (include boolean flag for init)
import math
import sqlite3
import time
import psycopg2
from psycopg2.extras import execute_values
from web3 import Web3
from datetime import datetime, timedelta
import requests
import pandas as pd
import src.helpers as helpers
import math
from duneanalytics import DuneAnalytics
import os

#database
def database_connect(dbname, user, password, host):
    con = psycopg2.connect(database = dbname, user = user, password = password, host = host, port = 5432, keepalives=1,
                        keepalives_idle=130,
                        keepalives_interval=10,
                        keepalives_count=15)
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS T360 (time varchar, price float8, id varchar, oracle varchar);")
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
    scale = 1e18
    for id in ids:
        tellor_data = contract.functions.getDataBefore(id, int(time.time()) - 50).call()
        timestamp = datetime.fromtimestamp(int(tellor_data[2]))
        if id == "0x0d12ad49193163bbbeff4e6db8294ced23ff8605359fd666799d4e25a3aa0e3a": # ID 10
            price = int.from_bytes(tellor_data[1], "big") / scale

        else:
            price = int.from_bytes(tellor_data[1], "big") / scale

        if price > 0:
            results.append((str(timestamp), price, id, 'tellor'))

        if init:
            old_date = (datetime.now() - timedelta(days = days_back))
        else:
            old_date = helpers.get_enddate('tellor', id)

        while old_date < datetime.fromtimestamp(tellor_data[2]):
            tellor_data = contract.functions.getDataBefore(id, tellor_data[2]).call()
            timestamp = datetime.fromtimestamp(int(tellor_data[2]))
            if price > 0:
                price = int.from_bytes(tellor_data[1], "big") / scale
            if id == 10:
                #if timestamp.hour == 0:
                results.append((str(timestamp), price / scale, id, 'tellor'))

            else:
                results.append((str(timestamp), price, id, 'tellor'))


#chainlink
def chainlink_grabdata(init, contract, id, days_back, results, con, scale = 1, inverse = False):
    latest_data = contract.functions.latestRoundData().call()
    if init:
        old_date = datetime.now() - timedelta(days = days_back)
    else:
        old_date = helpers.get_enddate('chainlink', id)

    if inverse:
        price = 1 / (latest_data[1] / scale)
    else:
        price = latest_data[1] / scale
    results.append((str(helpers.time_convert(latest_data[3])), price, id, "chainlink"))

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

        results.append((str(helpers.time_convert(past_data[3])), price, id, "chainlink"))

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
        old_date = helpers.get_enddate('ampleforth', 10)

    for i in range(0, len(new_timestamps)):
        if new_timestamps[i] > old_date:
            results.append((str(new_timestamps[i]), payload[i], 10, 'ampleforth'))


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
    #c.executemany("insert into tellor_datatable values(?, ?, ?, ?)", results)
    execute_values(c,'INSERT INTO T360 (time, price, id, oracle) VALUES %s', results)
    c.execute("DELETE FROM T360 WHERE PRICE = 0;")
    con.commit()
    con.close()