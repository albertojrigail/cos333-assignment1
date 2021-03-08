#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
import argparse

#-----------------------------------------------------------------------

def main(argv):  

    # set up argparse with optional arguments
    parser = argparse.ArgumentParser(description="Client for the registrar application")
    parser.add_argument('host', type=int, help="the host on which the server is running", nargs=1)
    parser.add_argument('port', type=int, help="the port at which the server is listening", nargs=1)

    # parse arguments
    arguments = parser.parse_args(argv[1:])
    host = arguments.host[0]
    port = arguments.port[1]

    


#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
