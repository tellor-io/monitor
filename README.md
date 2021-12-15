### To run:

 1. download directory by running: `git clone https://github.com/tellor-io/monitor.git`
 2. create virtual environment by running: `python3 -m venv dataquality`
 3. start venv by running: `source dataquality/bin/activate`
 4. once you're in folder and have everything set up, install needed dependencies by running: `pip install -r requirements.txt`
 5. use example.env file to create a .env file in the src directory including your infura endpoint
 
 The database file named tellor.db is in this directory and what you will be using. You can update it with more current values by running `python3 monitor.py`
 
 Finally, to view the data we've gotten, run `python3 tellor_dashboard.py`
 
 Your data will be available to see at http://127.0.0.1:8050/


