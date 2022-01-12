from bs4 import BeautifulSoup
import pandas as pd
import cloudscraper
from numpy import random
from time import sleep


# Get past transactions from etherscan:
# https://etherscan.io/address/0xe8218cacb0a5421bc6409e498d9f8cc8869945ea
# Navigate to the bottom of the page and click "Download CSV Export"

# Load csv into pandas dataframe
print('Loading in csv...')
df = pd.read_csv('~/tellor/monitor/data/oracle_txs_2022-01-12.csv', index_col=False)

# Drop unneeded columns
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
df.reset_index(drop=True, inplace=True)
print('Shape', df.shape)

# Add missing data columns
df['using_flashbots'] = False
df['reward_usd'] = .0
df['reward_trb'] = .0

# Scrape etherscan tx pages
scraper = cloudscraper.create_scraper()
pages = []

for i, (tx_hash, row) in enumerate(zip(df.txhash, df.index)):

    if i > 1990:
        sleep(random.uniform(.1, .3))  # Wait random time to help hide from bot detectorz
        print(f'i {i}, row {row}, tx hash {tx_hash}')
        url = f'https://etherscan.io/tx/{tx_hash}'
        tx_page = scraper.get(url).text
        pages.append((tx_page, row))

print('pages', len(pages))
# assert len(pages) == df.shape[0]

# Add Flashbots & reward data (TRB & USD) to dataframe
for (page, row) in pages:
    soup = BeautifulSoup(page, 'html.parser')

    # Identify Flashbots txs by looking for a Flashbots label,
    # an element with the class name below:
    found_fb = soup.find_all("a", {"class": "mb-1 mb-sm-0 u-label u-label--xs u-label--info"})

    # Change column value if using Flashbots
    if found_fb and "Flashbots" in found_fb[0].text:
        print(f'row {row} using flashbots')
        df.at[row,'using_flashbots'] = True
    
    # Find rewards element
    found_reward = soup.find_all("span", attrs={"data-original-title":True})

    if found_reward:
        # Extract rewards
        trb = float(found_reward[0].text)
        price_trb = found_reward[0]['data-original-title']
        price_trb = float(price_trb.replace('Current Price : $', '').replace(' / TRB', ''))

        # Save reward values
        df.at[row, 'reward_trb'] = trb
        df.at[row, 'reward_usd'] = trb * price_trb

# Verify scraped & saved data
for i in range(1991, 1997):
    print(f'i {i}')
    print(df.iloc[i])
    print(f'https://etherscan.io/tx/{df.iloc[i].txhash}')

# Export updated dataframe

