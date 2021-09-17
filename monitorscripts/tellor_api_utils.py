import time

import pandas as pd
import requests
import streamlit as st

#TELLOR API LINK (SUB THIS FOR BUILD 2)

class TellorAPIUtils:

    def __init__(self) -> None:
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

        #shape data from tellor api to json
        r = requests.get(self.tellor_api + str(request_id)).json()

        #shape json data to pandas dataframe
        df = pd.DataFrame(r)

        #return most recent timestamp
        last_timestamp = int(df['timestamp'].max())
        
        if request_id == 10:
            self.time_gap["red"] = 23*60*60
        
        print(time.time() - last_timestamp)
        request_id_dict = {
            "Request Id":request_id,
            "Seconds Since Last Update": time.time() - last_timestamp,
            "Status": "white"
        }

        if time.time() - last_timestamp >= self.time_gap["red"]:
            request_id_dict["Status"] = "red"
        elif time.time() - last_timestamp >= self.time_gap["yellow"]:
            request_id_dict["Status"] = "yellow"
        #MVP: show requestId and status
        return request_id_dict

        
if __name__ == "__main__":
    tau = TellorAPIUtils()
    tau.request_tellor_api(10)