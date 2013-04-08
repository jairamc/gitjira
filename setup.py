#!/usr/bin/env python

from distutils.core import setup 

setup(name='gitjira',
    version='0.2',
    author='Jairam Chandar & Michael Pitidis',
    author_email='contact@jairam.me',
    license='GPLv3',
    description='Tool to integrate Jira ticket information in git',
    scripts=['bin/gitjira'],
    packages=['gitjira'], 
    )
