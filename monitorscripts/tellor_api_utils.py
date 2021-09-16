import os
import time

import pandas as pd
import requests
from requests.api import request
import streamlit as st
from web3 import Web3
from web3.types import Timestamp

#TELLOR API LINK (SUB THIS FOR BUILD 2)

class TellorAPIUtils:

    def __init__(self, network) -> None:
        self.network = network
        self.tellor_api = "http://api.tellorscan.com/price/1/"
        self.time_gap = {
            "yellow": 12*60*60,
            "red": 24*60*60
        }

    def get_request_id_status(self, request_id:int):
        '''Calls tellor api data and finds most most recent timestamp on a request Id.
        Input: 
        request_id (int)
        Output:
        df (pandas.DataFrame)
        '''

        if self.network == "mainnet":
            return self.get_tellor_api(request_id)

        if self.network == "polygon":
            return self.get_mesosphere_data(request_id)

    def get_tellor_api(self, request_id:int):

        #shape data from tellor api to json
        r = requests.get(self.tellor_api + str(request_id)).json()

        #shape json data to pandas dataframe
        df = pd.DataFrame(r)

        #return most recent timestamp
        last_timestamp = int(df['timestamp'].max())
        
        if request_id == 10:
            self.time_gap["red"] = 23*60*60
        
        request_id_dict = {
            "Request Id":request_id,
            "Seconds Since Last Update": time.time() - last_timestamp,
            "Status": self.check_health(last_timestamp)
        }
        
        #MVP: show requestId and status
        return request_id_dict

    def get_mesosphere_data(self, request_id:int):

        address = "0xACC2d27400029904919ea54fFc0b18Bf07C57875"
        rpc_endpoint = "https://poly-mainnet.gateway.pokt.network/v1/lb/" + os.getenv('POKT_GATEWAY_URL')
        w3 = Web3(Web3.HTTPProvider(rpc_endpoint))
        tellor_mesosphere = w3.eth.contract(address, abi=open("abi.json").read())
        curr_value = tellor_mesosphere.functions.getCurrentValue(request_id).call()
        last_value = curr_value[1]
        last_timestamp = curr_value[2]

        self.time_gap["yellow"] = 5*60
        self.time_gap["red"] = 6*60*60

        request_id_dict = {
            "Request Id":request_id,
            "Seconds Since Last Update": time.time() - last_timestamp,
            "Status": self.check_health(last_timestamp)
        }

        return request_id_dict

    def check_health(self, last_timestamp):
        if time.time() - last_timestamp >= self.time_gap["red"]:
            return "urgent"
        elif time.time() - last_timestamp >= self.time_gap["yellow"]:
            return "warning"
        else:
            return "healthy"


        
if __name__ == "__main__":
    tau = TellorAPIUtils()
    tau.request_tellor_api(10)