

### To run:

 1. Download directory by running: `git clone https://github.com/tellor-io/monitor.git`
 2. Create virtual environment by running: `python3 -m venv dataquality`
 3. Start venv by running: `source dataquality/bin/activate`
 4. Install needed dependencies by running: `pip install -r requirements.txt`
 5. Use example.env file to create a .env file that includes your infura endpoint
 6. Run `python3 tellor_dashboard.py` to view the dashboard
    * Note: The database file named tellor.db is in this directory and what you will be using. You can update it with more current values by running `python3 monitor.py`
 7. Run `python3 monitor.py` to update the data on the dashboard, if needed.  
    * Note: to get accurate dune analytics data, copy this [query](https://dune.xyz/queries/136563). Change the date to when the last update to the database was. In the .env file, add the number in the url of your query as the DUNE_QUERY_ID
 8. Go to http://127.0.0.1:8050/ to view the dashboard locally


### File Structure 

#### Scripts
* helpers.py
  * helper functions to convert timestamps and retrieve datetime data from the database
* monitor.py
  * the main script that needs to be run consistently to upkeep the datastore
  * gets data from tellor, chainlink, ampleforth and makerDAO oracles
  * takes care of database maintenance start to finish
* datasource.py
  * main getter functions for retrieving data from different sources, as well as database communication functions
* tellor_dashboard.py
  * runs the frontend via plotly-dash of the app

#### Data
* tellor.db
  * where all sourced data is being stored
* ext_data.json
  * abi and address information for the chainlink and tellor contracts data is sourced from

#### Other Files
* .env / example.env
  * all private information the app wll need to run and get access to certain services like an infura node and dune analytics
* requirements.txt
  * all app dependencies that need to be installed




 




