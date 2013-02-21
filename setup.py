#!/usr/bin/env python

from distutils.core import setup 

setup(name='gitjira',
    version='0.2',
    author='Jairam Chandar',
    author_email='jairamc23@gmail.com',
    license='GPLv3',
    description='Tool to integrate Jira ticket information in git',
    scripts=['bin/gitjira'],
    packages=['gitjira'], 
    )