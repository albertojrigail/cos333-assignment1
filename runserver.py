#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv, exit, stderr
from regserver import app
import argparse

def main(argv):
    # argument parsing
    parser = argparse.ArgumentParser(description="The registrar application")
    parser.add_argument('port', type=int, help="the port at which the server should listen", nargs=1)
    arguments = parser.parse_args(argv[1:])
    port = arguments.port[0]
    
    try:
        app.run(host='0.0.0.0', port=port)

    except Exception:
        print("Address already in use", file=stderr)
        exit(1)
        

if __name__ == '__main__':
    main(argv)
