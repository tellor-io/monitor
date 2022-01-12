import pandas as pd


df_orig = pd.read_csv('~/tellor/monitor/etherscan_tx_data.csv', index_col=False)
df_missing1 = pd.read_csv('~/tellor/monitor/combined1.csv', index_col=False)
# df_missing2 = pd.read_csv('~/tellor/monitor/missing_tx_data2.csv', index_col=False)

print('Shape', df_orig.shape)
print('Shape', df_missing1.shape)
# print('Shape', df_missing2.shape)

df_no_reverts = df_orig.loc[df_orig['errcode'] != 'Reverted']
total_reverts = len(df_orig) - len(df_no_reverts)
print('Number of reverted transactions:', total_reverts)

df_missing = df_no_reverts.loc[df_no_reverts['reward_usd'] == .0]
print(df_missing.shape)
print('Number rows missing rewards data:', len(df_missing))

for i in range(len(df_missing1)):
    # Find overlapping values
    idx = df_orig.index[df_orig['txhash'] == df_missing1.iloc[i]['txhash']].tolist()[0]

    # Update missing values
    df_orig.at[idx, 'using_flashbots'] = df_missing1.iloc[i]['using_flashbots']
    df_orig.at[idx, 'reward_trb'] = df_missing1.iloc[i]['reward_trb']
    df_orig.at[idx, 'reward_usd'] = df_missing1.iloc[i]['reward_usd']

print()
print('After filling in missing values...')
df_no_reverts = df_orig.loc[df_orig['errcode'] != 'Reverted']
total_reverts = len(df_orig) - len(df_no_reverts)
print('Number of reverted transactions:', total_reverts)

df_missing = df_no_reverts.loc[df_no_reverts['reward_usd'] == .0]
print(df_missing.shape)
print('Number rows missing rewards data:', len(df_missing))

df_orig.to_csv('combined2.csv', index=True)
