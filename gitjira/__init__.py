#################################################################################
#
#    Copyright 2013 Jairam Chandar
#  
#    This file is part of GitJira.
#
#    GitJira is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GitJira is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GitJira.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

"""
Module for creating/updating git branches based on Jira tickets
"""

import urllib2, base64, json, subprocess, re, os
import transitions


def createUserHash(username, password):
	return base64.b64encode((username + ":" + password).encode('ascii'))

def readConfig(filename, sep='='):
    with open(filename, 'rb') as f:
        for line in f:
            yield [token.strip() for token in line.split(sep, 1)]

def readValidateConfig(filename, keys=('base_url', 'userhash')):
    data = dict(readConfig(filename))
    missing = [k for k in keys if not k in data]
    if missing:
        raise ValueError("Fields [%s] missing from configuration file" % ', '.join(`k` for k in missing))
    return data

def callJira(ticket, config):
    return json.load(jiraRequest(config, restIssue(ticket)))

def transitionTicket(ticket, transitionId, config):
    data = json.dumps(dict(transition=dict(id=transitionId)))
    path = restIssue(ticket, 'transitions?expand=transitions.fields')
    return json.load(jiraRequest(config, path, data))

def getBranch():
    regex = re.compile('^\w+/[^-]+-\w+$')
    cmd = ['git', 'status']
    statusMsg = subprocess.check_output(cmd)
    branch = statusMsg.split('\n')[0].split("# On branch ")[1]
    if not regex.match(branch):
        raise GitBranchError("Not on valid gitjira branch")
    return branch

def createBranch(ticket, config, transition = True):
	response = callJira(ticket, config)

	key = response['key']
	issueType = response['fields']['issuetype']['name']
	branchname = issueType.lower() + "/" + key

	cmd = ['git', 'checkout', '-b', branchname]
	subprocess.check_call(cmd)

	if (transition == True):
		transitionTicket(ticket, transitions.in_progress, config)

def commitBranch(config):
	branch = getBranch()
	ticket = branch.split('/')[1]

	response = callJira(ticket, config)

	msg = response['key'] + " - " + response['fields']['summary']
	msg = msg + "\n#TO ABORT THIS COMMIT, DELETE THE COMMIT MESSAGE ABOVE AND SAVE THIS FILE!"

	cmd = ['git', 'commit', '-m', msg, '-e']
	subprocess.call(cmd)


def jiraRequest(config, path, data=None):
    """Build and perform a request to the JIRA API."""
    url = os.path.join(config['base_url'], path)
    headers = {'Authorization': 'Basic %s' % config['userhash'],
               'Content-Type' : 'application/json'}
    request = urllib2.Request(url, data, headers)
    reply = urllib2.urlopen(request)
    if reply.getcode() >= 400:
        raise HTTPError("Request failed with status %d, url: %s" % (reply.getcode(), url))
    return reply

def restIssue(*parts):
    assert all(not part.startswith('/') for part in parts), "Expecting relative path"
    return os.path.join('rest/api/latest/issue', *parts)


class GitJiraError(Exception):
    pass

class HTTPError(GitJiraError):
    pass

class GitError(GitJiraError):
    pass

class GitBranchError(GitError):
    pass

