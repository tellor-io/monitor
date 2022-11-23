from bs4 import BeautifulSoup
import pandas as pd
import cloudscraper
from numpy import random
from time import sleep


# WARNING -- this script takes ~15 min to run

# Get past transactions from etherscan:
# https://etherscan.io/address/0xe8218cacb0a5421bc6409e498d9f8cc8869945ea
# Navigate to the bottom of the page and click "Download CSV Export"

# Load csv into pandas dataframe
print('Loading in csv...')
df_txs = pd.read_csv('~/Desktop/tellor/monitor/data/export-0xe8218cacb0a5421bc6409e498d9f8cc8869945ea.csv', index_col=False)

# Drop unneeded columns
print('Dropping columns...')
df_txs.drop([
    'Blockno', 'UnixTimestamp', 'ContractAddress',
    'To', 'Value_IN(ETH)', 'Value_OUT(ETH)',
    'CurrentValue @ $2687.26/Eth', 'TxnFee(ETH)',
    'Historical $Price/Eth'],
    axis=1,
    inplace=True)

df_txs.columns = [name.lower() for name in df_txs.columns]
print(df_txs.iloc[2])
print('Shape', df_txs.shape)

# Keep only submitValue() transactions
print('Dropping tipping txs...')
df_txs = df_txs.loc[df_txs['method'] == 'Submit Value']
df_txs.reset_index(drop=True, inplace=True)
print('Shape', df_txs.shape)

# Add missing data columns
df_txs['using_flashbots'] = False
df_txs['reward_usd'] = .0
df_txs['reward_trb'] = .0

def scrape_and_save(df, filename):
    # Scrape etherscan tx pages
    scraper = cloudscraper.create_scraper()
    pages = []

    # LOOP ONE
    for i, (tx_hash, row) in enumerate(zip(df.txhash, df.index)):
        print(i)
        # if i > 1990:
        sleep(random.uniform(.1, .3))  # Wait random time to help hide from bot detectorz
        # print(f'i {i}, row {row}, tx hash {tx_hash}')
        url = f'https://etherscan.io/tx/{tx_hash}'
        tx_page = scraper.get(url).text
        pages.append((tx_page, row))

    print('pages', len(pages))

    # LOOP TWO
    # Add Flashbots & reward data (TRB & USD) to dataframe
    for (page, row) in pages:
        print('page,row')
        soup = BeautifulSoup(page, 'html.parser')

        # Identify Flashbots txs by looking for a Flashbots label,
        # an element with the class name below:
        found_fb = soup.find_all("a", {"class": "mb-1 mb-sm-0 u-label u-label--xs u-label--info"})

        # Change column value if using Flashbots
        if found_fb and "Flashbots" in found_fb[0].text:
            print("found flashbots")
            df.at[row,'using_flashbots'] = True
        
        # Find rewards element
        found_reward = soup.find_all("span", attrs={"data-original-title":True})

        if found_reward:
            # Extract rewards
            print("extract rewards")
            trb = float(found_reward[0].text)
            price_trb = found_reward[0]['data-original-title']
            price_trb = float(price_trb.replace('Current Price : $', '').replace(' / TRB', ''))

            # Save reward values
            df.at[row, 'reward_trb'] = trb
            df.at[row, 'reward_usd'] = trb * price_trb

        # Verify scraped & saved data
        # for i in range(1991, 1997):
        #     print(f'i {i}')
        #     print(df.iloc[i])
        #     print(f'https://etherscan.io/tx/{df.iloc[i].txhash}')

    # Export updated dataframe
    df.to_csv(filename, index=False)
    print('Saved scraped data')

    assert len(pages) == df.shape[0]

scrape_and_save(df_txs, 'etherscan_tx_data.csv')

# WARNING -- this script takes ~15 min or longer to run
