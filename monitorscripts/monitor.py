import pandas as pd

class Monitor:

    def __init__(self, networks, request_ids) -> None:
        self.networks = []
        self.request_ids = []

        self.status_df = pd.DataFrame()
        
    def add_request_id(self, request_id:int) -> None:
        '''Adds request ids for parsing'''
        self.request_ids.append(request_id)

    def make_monitor_dataframe(self):
        '''Creates monitor for display using streamlit'''


        #display streamlit table
    
