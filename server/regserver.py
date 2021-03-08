#!/usr/bin/env python

#-----------------------------------------------------------------------
# regserver.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import exit, argv, stderr
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from pickle import dump
from server.getcourse import getCourse
from server.getclassdetails import getClassDetails

#-----------------------------------------------------------------------

def handleClient(sock):
    inFlo = sock.makefile(mode='r', encoding='utf-8')
    outFlo = sock.makefile(mode='wb')
    request = inFlo.readline()
    arguments = inFlo.readline()

    # call helper functions, and dump requested objects
    if request == "course":
        courses = getCourse(arguments)
        dump(courses, outFlo)
    elif request == "classDetails":
        classDetails = getClassDetails(arguments)
        dump(classDetails, outFlo)
    else:
        raise Exception("Message is empty")
    
    outFlo.flush()
    print("Wrote " + request + " to client")
 
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
                print('Accepted connection for ' + str(clientAddr))
                print('Opened socket for ' + str(clientAddr))
                handleClient(sock)
                sock.close()
                print('Closed socket for ' + str(clientAddr))
            except Exception as e:
                print(e, file=stderr)
    except Exception as e:
        print(e, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
