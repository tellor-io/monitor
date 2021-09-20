from typing import Dict
import pandas as pd
import streamlit as st

from tellor_api_utils import TellorAPIUtils

class Monitor:

    def __init__(self, curr_monitored_ids:Dict) -> None:
       
        self.curr_monitored_ids = curr_monitored_ids
        self.tau = TellorAPIUtils()

        self.status_df = pd.DataFrame()
        
    def add_request_id(self, request_id:int) -> None:
        '''Adds request ids for parsing'''
        self.request_ids.append(request_id)

    def make_monitor_dataframe(self):
        '''Creates monitor for display using streamlit'''
        
        list_of_dicts = []

        for network in self.curr_monitored_ids.keys():
            for request_id in self.curr_monitored_ids[network]:
                #add request Id status to df
                request_id_dict = self.tau.get_request_id_status(request_id, network)

                list_of_dicts.append(request_id_dict)
        
        self.status_df = pd.DataFrame(list_of_dicts)
        
        #apply coloring
        self.status_df = self.status_df.style.applymap(self.map_status)
        
        #display streamlit table
        st.dataframe(self.status_df)

    def map_status(self, status:str):
        if status == "urgent":
            return "background-color: red"
        elif status == "warning":
            return "backgrond-color: yellow"
        else:
            return "backgrond-color: white"

            
