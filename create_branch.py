#! /usr/bin/env python

import urllib2, base64, config, sys, json, subprocess, os


def usage():
	return "Usage - \n\tcreate_branch.py <ticket>"

def createBranch(branchname):
	cmd = ['git', 'checkout', '-b', branchname]
	subprocess.check_call(cmd)

if (config.username == '' or config.password == ''):
    print "Username or Password not provided"
    sys.exit(1)

if (len(sys.argv) < 2):
	print usage()
	sys.exit(1)

ticket = sys.argv[1]
url = config.base_url + '/rest/api/latest/issue/' + ticket


userHash = base64.b64encode((config.username+":"+config.password).encode('ascii'))
opener = urllib2.build_opener()
opener.addheaders = [('Authorization', 'Basic ' + userHash)]

response = json.load(opener.open(url))

key = response['key']
comment = response['fields']['summary'].split()[0:5]

createBranch(key+"-"+"-".join(comment))