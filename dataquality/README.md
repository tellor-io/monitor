### To run:

 1. download directory by running: `git clone https://github.com/tellor-io/monitor.git`
 2. create virtual environment by running: `python3 -m venv dataquality`
 3. start venv by running: `source dataquality/bin/activate`
 4. enter the data quality folder as your working directory
 5. once you're in folder and have everything set up, install needed dependencies by running: `pip install -r requirements.txt`
 
 Now you're ready to strt building the database. This structure only needs to initialize the database once. To do this, run `python3 db_init.py`. This takes a while, as it's getting data from the past 60 days.
 
 After this, whenever you want to add values to the database, you can update it by running `python3 db_update.py`
 
 Finally, to view the data we've gotten, run `python3 dashboard_draft2.py`
 
 Your data will be available to see at http://127.0.0.1:8050/
