import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd

# etherscan_key = os.getenv('ETHERSCAN_KEY')

# Get tx hashes
# hashes_request_url = f'https://api.etherscan.io/api?module=account&action=txlist&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a&startblock=0&endblock=99999999&offset=10&sort=asc&apikey={etherscan_key}'

# hashes = requests.get(hashes_request_url).json()['result']
# print(hashes)

# txn_hash = '0xe267acf0823f30513159c500f9e362a6afd20dad62b2bc4140be11f5101b4e88'
# revert_count = 0
# for tx_hash in hashes:
#     print(json.dumps(tx_hash, indent=4))
#     time.sleep(.1)

#     etherscan_url = 'https://api.etherscan.io/api?module=transaction&action=getstatus&txhash={0}&apikey={1}'.format(tx_hash, etherscan_key)

#     r = requests.get(etherscan_url)
#     files = r.json()

    
#     if files['result']['errDescription'] == 'Reverted':
#         revert_count+=1

# print('revert count:', revert_count)

# oracle_page = requests.get('https://etherscan.io/address/0xe8218cacb0a5421bc6409e498d9f8cc8869945ea')
# soup = BeautifulSoup(oracle_page.text, 'html.parser')

# soup.


# Get past transactions
# Load csv into pandas dataframe
print('Loading in csv...')
df = pd.read_csv('~/tellor/monitor/data/oracle_txs_2022-01-12.csv', index_col=False)

# Get rid of unneeded columns
print('Dropping columns...')
df.drop([
    'Blockno', 'UnixTimestamp', 'ContractAddress',
    'To', 'Value_IN(ETH)', 'Value_OUT(ETH)',
    'CurrentValue @ $3229.05/Eth', 'TxnFee(ETH)',
    'Historical $Price/Eth'],
    axis=1,
    inplace=True)

df.columns = [name.lower() for name in df.columns]
print(df.iloc[2])
print('Shape', df.shape)

# Keep only submitValue() transactions
print('Dropping tipping txs...')
df = df.loc[df['method'] == 'Submit Value']
print('Shape', df.shape)


for i, tx_hash in enumerate(df.txhash):
    print(f'row {i}, tx hash {tx_hash}')
# Iterate through tx hashes and 
# fetch using-flashbots bool by scraping that etherscan page for that label
# and also fetch the reward in TRB & USD and historical price of TRB at the time
# Add bool to column in dataframe

# Export dataframe to csv

# Rows of submitValue txs
# Columns: 
# Tx num (nonce?), Date/time, reward TRB, reward USD, total fees paid ETH, ..
# .. total fees paid USD, using Flashbots (bool), reporter address, tx status (reverted?),



