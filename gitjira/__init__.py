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
Module for creating/updating git branches based on Jira tickets.
"""

import base64, re

from git import Git
from error import GitBranchError


def createUserHash(username, password):
    return base64.b64encode((username + ":" + password).encode('ascii'))


def getBranch():
    regex = re.compile('^\w+/[^-]+-\w+$')
    branch = Git().status().split('\n')[0].split("# On branch ")[1]
    if not regex.match(branch):
        raise GitBranchError("Not on valid gitjira branch")
    return branch


def createBranch(ticket, jira, transition=True):
    response = jira.ticket(ticket)

    key = response['key']
    issueType = response['fields']['issuetype']['name']
    branchName = '%s/%s' % (issueType.lower(), key)

    Git().branch(branchName)

    if transition:
        jira.mark_in_progress(ticket)


def commitBranch(jira):
    branch = getBranch()
    ticket = branch.split('/')[1]

    response = jira.ticket(ticket)

    msg = '%s - %s\n\n# TO ABORT THIS COMMIT, DELETE THE COMMIT MESSAGE ABOVE AND SAVE THIS FILE!' \
            % (response['key'], response['fields']['summary'])

    Git().commit(msg)

