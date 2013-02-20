git-jira
========

Script to create a branch based on a Jira ticket

Installation
---------------
Clone the repo.

```console
git clone git@github.com:jairamc/git-jira.git 
```

Create symlink so its available everywhere
```console
ln -s /usr/local/bin/create_branch <path-to-folder>/git-jira/create_branch.py
```


Usage
---------------
In the installed folder, you will find a config.py file. Update with user credentials. The ```base_url``` is url to your Jira installation. For eg. ```https://jira.atlassian.net```. This should be an ```https``` link.


Run it from within your repo, i.e., you should be in the folder where you have your code.

```console
prompt> create_branch <ticket-number>
```
In the current version, it will fetch the ticket type and create a branch ```<issue type>/<ticket number>```. Await improvements!
