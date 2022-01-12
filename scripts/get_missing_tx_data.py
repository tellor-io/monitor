from bs4 import BeautifulSoup
import pandas as pd
import cloudscraper
from numpy import random
from time import sleep
from get_oracle_tx_data import scrape_and_save

# Load csv into pandas dataframe
print('Loading in csv...')
df = pd.read_csv('~/tellor/monitor/missing_tx_data3.csv', index_col=False)

print(df.iloc[2])
print('Shape', df.shape)

df_no_reverts = df.loc[df['errcode'] != 'Reverted']
total_reverts = len(df) - len(df_no_reverts)
print('Number of reverted transactions:', total_reverts)

df_missing = df_no_reverts.loc[df_no_reverts['reward_usd'] == .0]
print(df_missing.shape)
print('Number rows missing rewards data:', len(df_missing))

# fill in missing values
scrape_and_save(df_missing, 'missing_tx_data4.csv')

