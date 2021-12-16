### To run:

 1. download directory by running: `git clone https://github.com/tellor-io/monitor.git`
 2. create virtual environment by running: `python3 -m venv venv`
 3. start venv by running: `source venv/bin/activate`
 4. install needed dependencies by running: `pip install -r requirements.txt` (this may take awhile)
 5. use example.env file to create a .env file in the monitor directory including your infura endpoint
 
 The database file named tellor.db is in the data directory and is what the dashboard script will be pulling data from. You can update it with current values by running `python3 data/monitor.py`
 
 Finally, to view the data, run `python3 scripts/tellor_dashboard.py`
 
 The dashboard will be available to see at http://127.0.0.1:8050/


