#!/usr/bin/env python

#-----------------------------------------------------------------------
# regserver.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import exit, argv, stderr
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from pickle import dump, load
from getcourse import getCourse
from getclassdetails import getClassDetails
import argparse

#-----------------------------------------------------------------------

def handleClient(sock):
    inFlo = sock.makefile(mode='rb')
    incoming = load(inFlo)
    request = incoming[0]
    arguments = incoming[1]
    outFlo = sock.makefile(mode='wb')

    # call helper functions, and dump requested objects
    print("Received command: " + request)
    print("Received argumments: " + arguments)
    if request == "getOverviews":
        courses = getCourse(arguments)
        dump(courses, outFlo)
    elif request == "getDetail":
        classDetails = getClassDetails(arguments)
        dump(classDetails, outFlo)

    # send information back
    outFlo.flush()
 
#-----------------------------------------------------------------------

def main(argv):
    # PARSE ARGUMENTS
    parser = argparse.ArgumentParser(description="Server for the registrar application")
    parser.add_argument('port', type=int, help="the port at which the server should listen", nargs=1)
    arguments = parser.parse_args(argv[1:])
    port = arguments.port[0]

    # RUN SERVER
    try:
        port = int(argv[1])
        serverSock = socket()
        print('Opened server socket')
        serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSock.bind(('', port))
        print('Bound server socket to port')
        serverSock.listen()
        print('Listening')
        while True:
            try:
                sock, clientAddr = serverSock.accept()
                print('Accepted connection, opened socket')
                handleClient(sock)
                sock.close()
                print('Closed socket')
            except Exception as e:
                print("Handling exception!")
                print(argv[0] + ":", e, file=stderr)

    except Exception as e:
        print(argv[0] + ":", e, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
