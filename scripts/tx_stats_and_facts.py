import pandas as pd


df = pd.read_csv('~/tellor/monitor/combined2.csv', index_col=False)
print(list(df.columns))

########################## OVERVIEW STATS ############################
print()
print('******** OVERVIEW ********')

print('Total number of submitValue transactions from 12/01/21 to 01/12/22:', len(df))

df_no_reverts = df.loc[df['errcode'] != 'Reverted']
success_txs = len(df_no_reverts)
percent_success = round(success_txs / len(df) * 100)
print(f'Total successful transactions: {success_txs} or {percent_success}%')

total_reverts = len(df) - success_txs
print(f'Total reverted transactions: {total_reverts} or {100 - percent_success}%')

df_missing = df_no_reverts.loc[df_no_reverts['reward_usd'] == .0]
percent_missing = round(len(df_missing) / len(df) * 100, 2)
print(f'Total successful transactions with zero reward: {len(df_missing)} or {percent_missing}%')

total_trb_reward = df.reward_trb.sum()
total_usd_reward = df.reward_usd.sum()
total_usd_commas = "{:,}".format(round(total_usd_reward))
print(f'Total rewards given to reporters: {round(total_trb_reward)} TRB or ${total_usd_commas}')

total_fees = df['txnfee(usd)'].sum()
total_fees_commas = "{:,}".format(round(total_fees))
print('Total transaction fees paid: $' + total_fees_commas)

total_profit_commas = "{:,}".format(round(total_usd_reward - total_fees))
print(f'Total reporter profit: ${total_profit_commas}')

total_reporters = df_no_reverts['from'].nunique()
print('Total reporters:', total_reporters)  # have submitted successfully, not necessarily at profit

######################### MORE STATS #################################
print()
print('******** MORE STATS ********')

######################### FLASHBOTS #################################
print()
print('******** FLASHBOTS ********')

