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

if __name__ == '__main__':
    try:
        use_casperjs()
    except KeyboardInterrupt:
        print("Exiting.")
        sys.exit(1)
