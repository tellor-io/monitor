# Tellor processes monitor

This repository holds all the scripts to monitor Tellor's automated processes.

## Installation

### Installing pipenv
If you do not have [pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) package manager installed:
`pip3 install --user pipenv`

#### Add pipenv to path
Unfortuntely, pipenv won't work until you add it to PATH. Here's how to do so on...

Linux:
https://askubuntu.com/questions/1113806/how-can-i-add-local-bin-to-my-path

Mac:
Add the python 3.8 to PATH.
1. Run the following command: `sudo nano /etc/paths`
2. Enter your password, when prompted
3. Go to the bottom of the file, and enter the path you wish to add.
    a. /Users/username*/Library/Python/3.8/bin
      *replace the 'username' with the actual user name
4. Hit control + x to quit
5. Enter “Y” to save the modified buffer
6. Press Esc
7. Enter "A" to append
8. Press Enter

If the above doesn't work, try:
1. Run the following command: `sudo nano ~/.zshrc`
2. Enter your password, when prompted
3. in the .zshrc file, paste the following: `path+=('~/Library/Python/3.8/bin')`
4. exit `nano`  (use Ctrl + x)
5. Enter “Y” to save the modified buffer
6. Press Esc
7. Enter "A" to append
8. Press Enter
9. `source ~/.zshrc`



### If pipenv is already installed
If you have `pipenv` installed already:
`pipenv install`

## Starting the dashboard

`pipenv run streamlit run monitorscripts/run.py`
