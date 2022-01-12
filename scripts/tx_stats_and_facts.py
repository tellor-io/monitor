import pandas as pd
import matplotlib.pyplot as plt


def plot(groupby, xlbl, ylbl):
    groupby.plot(kind='bar')
    plt.xlabel(xlbl)
    plt.ylabel(ylbl)

    ax = plt.gca()
    ax.axes.xaxis.set_ticks([])

    plt.show()


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

df['time_diff'] = pd.to_datetime(df['datetime'],format='%Y-%m-%d %H:%M:%S')
df['time_diff'] = df['time_diff'].diff().fillna(method='backfill').apply(lambda x: x.total_seconds()/60)
df.index = pd.to_datetime(df['datetime'],format='%Y-%m-%d %H:%M:%S')
weeks = df.groupby(pd.Grouper(freq='W'))
total_txs_per_wk = weeks.size()
print(f'change in number of submitValue txs per week:')
print(total_txs_per_wk)
# plot(total_txs_per_wk, 'weeks', 'num txs')

weekly_gains = weeks['reward_usd'].sum()
weekly_losses = weeks['txnfee(usd)'].sum()
weekly_profit = weekly_gains - weekly_losses
print(f'change in profit per week:')
print(weekly_profit)
# plot(weekly_profit, 'weeks', 'USD (rewards - fees)')

unique_reporters_per_week = weeks['from'].nunique()
print(f'unique reporters per week:')
print(unique_reporters_per_week)
# plot(unique_reporters_per_week, 'weeks', 'num reporters')

print(f'time between value updates:')
weekly_avg_update_time = weeks['time_diff'].mean()
print(weekly_avg_update_time)
# plot(weekly_avg_update_time, 'weeks', 'average minutes between submitValue txs')

# TODO: fix
# top_10_freq = weeks['from'].agg(lambda x: x.value_counts()[:10].sum())
# below_top_10_freq = weeks['from'].agg(lambda x: x.value_counts()[10:].sum())
# weekly_percent_top_10 = round(top_10_freq / below_top_10_freq)
# plot(weekly_percent_top_10, 'weeks', 'percent')

# print(f'top ten percent most frequent reporters total profit per week:')

######################### FLASHBOTS #################################
print()
print('******** FLASHBOTS ********')

num_flashbots_txs = len(df.loc[df['using_flashbots'] == True])
percent_flashbots_txs = round(num_flashbots_txs / len(df) * 100)
print(f'Total txs sent using Flashbots: {num_flashbots_txs} or {percent_flashbots_txs}%')

reverts = df.loc[df['errcode'] == 'Reverted']
failed_flashbots = len(reverts.loc[reverts['using_flashbots'] == True])
percent_failed_flashbots = round(failed_flashbots / total_reverts * 100, 2)
print(f'Total failed transactions using Flashbots: {failed_flashbots} or {percent_failed_flashbots}%')

flashbot_txs_per_wk = weeks.using_flashbots.sum()
# print(flashbot_txs_per_wk)
percent_fb_per_wk = round(flashbot_txs_per_wk / total_txs_per_wk * 100)
print(f'Change in Flashbots usage per week:')
print(percent_fb_per_wk)
plot(percent_fb_per_wk, 'weeks', 'percent')

# reversions_per_week = weeks.loc[weeks['errcode'] == 'Reverted'].sum()
reverts_per_wk = weeks['errcode'].apply(lambda x: x[x == 'Reverted'].count())
# print(reverts_per_week)
percent_reverts_per_wk = round(reverts_per_wk / total_txs_per_wk * 100)
print(f'Change in tx reversions per week')
print(percent_reverts_per_wk)
plot(percent_reverts_per_wk, 'weeks', 'percent')
