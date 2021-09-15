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
- `sudo nano ~/.zshrc`
- in the .zshrc file, paste the following:
`path+=('~/Library/Python/3.8/bin')`
- exit `nano`
- `source ~/.zshrc`

### If pipenv is already installed
If you have `pipenv` installed already:
`pipenv install`

## Starting the dashboard

`pipenv run streamlit run monitorscripts/monitor.py`
