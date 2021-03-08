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

#-----------------------------------------------------------------------

def handleClient(sock):
    print("handleClient(sock)")
    inFlo = sock.makefile(mode='rb')
    incoming = load(inFlo)
    request = incoming[0]
    arguments = incoming[1]
    outFlo = sock.makefile(mode='wb')

    # call helper functions, and dump requested objects
    print("Received command: " + request)
    if request == "getOverviews":
        courses = getCourse(arguments)
        dump(courses, outFlo)
    elif request == "getDetail":
        classDetails = getClassDetails(arguments)
        dump(classDetails, outFlo)
    else:
        raise Exception("Message is empty")

    # send information back
    outFlo.flush()
 
#-----------------------------------------------------------------------

def main(argv):

    if len(argv) != 2:
        print('Usage: python %s port' % argv[0])
        exit(1)

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
                print(argv[0] + ": " + e, file=stderr)

    except Exception as e:
        print(e, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
