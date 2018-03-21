#!/usr/bin/env python3
"""Periodically forget Facebook interaction data."""

import subprocess
import sys

import scrapy

def use_casperjs():
    """Launch casper script to access Facebook"""
    try:
        subprocess.call(['node_modules/casperjs/bin/casperjs', 'first-commit.js'])
    except FileNotFoundError:
        print("Couldn't find node_modules/casperjs/bin/casperjs in local directory.")
        sys.exit(1)

def get_facebook_session_token(email, password):
    """Submit credentials to Facebook's login and retrive the session token."""
    url = 'https://facebook.com'
    my_data = {'email': email, 'pass': password}
    request = scrapy.Request(url, method='POST',
                          body=json.dumps(my_data),
                          headers={'Content-Type':'application/json'})


if __name__ == '__main__':
    try:
        forget()
    except KeyboardInterrupt:
        print("Exiting.")
        sys.exit(1)
