GitJira
========

Script to create a branch based on a Jira ticket

Installation
---------------
#### Download

##### Either clone the repo - 
```console
git clone git@github.com:jairamc/git-jira.git 
```

##### Or download latest tag
```console
tar -xvzf git-jira.tar.gz
```
or
```console
unzip git-jira.zip
```

#### Install the package

##### Global install
```console
cd <path-to-code>
python setup.py install
```
The last step needs to be run as root if you want to install gitjira for all users. If you prefer a local installation — which is recommended at present, since there is no simple way to uninstall it — you can instead run the following commands as a user:

##### Local Install
```console
cd <path-to-code>
python setup.py install --home=~/local
```
installing locally will require the below steps as well 

```console
export PATH=$PATH:$HOME/local/bin
export PYTHONPATH=$HOME/local/lib/python
```

Features
---------------

- Create branches of the format - ```<issue type>/<ticket number>``` - given just the ticket id
- Automatically transition tickets to in-progress when you create a branch for a ticket
- Fetch the summary of a ticket and add to commit message when committing a branch created by gitjira

Usage
---------------
Run 
```console
prompt> gitjira -h
```
In the current version, branches are created in format ```<issue type>/<ticket number>```. Await improvements!


##### Special thanks to @mpitid (https://github.com/mpitid) for his help. 
