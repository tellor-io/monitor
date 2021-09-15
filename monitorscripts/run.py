from monitor import Monitor

current_monitored_ids = [1, 2, 10]

m = Monitor()

for i in current_monitored_ids:
    m.add_request_id(i)

m.make_monitor_dataframe()