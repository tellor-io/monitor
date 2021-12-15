### To run:

 1. Download directory by running: `git clone https://github.com/tellor-io/monitor.git`
 2. Create virtual environment by running: `python3 -m venv dataquality`
 3. Start venv by running: `source dataquality/bin/activate`
 4. Install needed dependencies by running: `pip install -r requirements.txt`
 5. use example.env file to create a .env file that includes your infura endpoint
 
 The database file named tellor.db is in this directory and what you will be using. You can update it with more current values by running `python3 monitor.py`
 
 Finally, to view the data run `python3 tellor_dashboard.py`
 
 Your data will be available to see at http://127.0.0.1:8050/


