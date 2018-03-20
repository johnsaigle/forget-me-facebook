#!/usr/bin/env python3
"""Periodically forget Facebook interaction data."""

import subprocess
import getpass

def forget():
    """Launch casper script to access Facebook"""
    try:
        subprocess.call(['node_modules/casperjs/bin/casperjs', 'first-commit.js'])
    except KeyboardInterrupt:
        print("Got CTRL-C. Exiting.")
        sys.exit(1)

if __name__ == '__main__':
    forget()
