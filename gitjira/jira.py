
"""
Handle requests to Jira.
"""

import os
import json
import urllib2

from error import HTTPError


class Workflow(object):
    BACKLOG     = 11
    IN_PROGRESS = 31
    REVIEW      = 81
    DONE        = 41


class Jira(object):
    """Perform requests to Jira's REST API."""

    def __init__(self, conf):
        self.conf = conf

    def ticket(self, ticket):
        return self.get(self._api(ticket))

    def mark_in_progress(self, ticket):
        path = self._api(ticket,'transitions?expand=transitions.fields')
        data = json.dumps(dict(transition=dict(id=Workflow.IN_PROGRESS)))
        return self.post(path, data)

    def join(self, *parts):
        assert all(not part.startswith('/') for part in parts), "Expecting relative path"
        return os.path.join(*parts)

    def get(self, path):
        return self._request(path)

    def post(self, path, data):
        return self._request(path, data)

    def _api(self, *parts):
        return self.join('rest/api/latest/issue', *parts)

    def _request(self, path, data=None):
        """Build and perform a request to the JIRA API."""
        url = self.join(self.conf.base_url, path)
        headers = {'Authorization': 'Basic %s' % self.conf.userhash,
                   'Content-Type' : 'application/json'}

        request = urllib2.Request(url, data, headers)
        reply = urllib2.urlopen(request)

        if reply.getcode() >= 400:
            raise HTTPError("Request failed with status %d, url: %s" % (reply.getcode(), url))
        return json.load(reply)


