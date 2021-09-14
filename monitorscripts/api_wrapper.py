import pandas as pd
import requests

#TELLOR API LINK (SUB THIS FOR BUILD 2)

class TellorAPIUtils:

    def __init__(self) -> None:
        self.tellor_api = "http://api.tellorscan.com/price/1/"

    def request_tellor_api(self, request_id:int):
        '''Shapes tellor api data into pandas DataFrame.
        Input: 
        request_id (int)
        Output:
        df (pandas.DataFrame)
        '''

        #shape data from tellor api to json
        r = requests.get(self.tellor_api + request_id).json()

        #shape json data to pandas dataframe

        #convert unix time (in seconds) to pandas datetime

    def 