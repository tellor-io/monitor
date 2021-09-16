import pandas as pd
import streamlit as st

from tellor_api_utils import TellorAPIUtils

class Monitor:

    def __init__(self, network) -> None:
        self.networks = network
        self.request_ids = []
        self.tau = TellorAPIUtils(network)

        self.status_df = pd.DataFrame()
        
    def add_request_id(self, request_id:int) -> None:
        '''Adds request ids for parsing'''
        self.request_ids.append(request_id)

    def make_monitor_dataframe(self):
        '''Creates monitor for display using streamlit'''
        
        list_of_dicts = []

        for i in self.request_ids:
            #add request Id status to df
            request_id_dict = self.tau.get_request_id_status(i)

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

            
