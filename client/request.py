#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from socket import socket
from pickle import load, dump

#-----------------------------------------------------------------------
def sendRequest(host, port, requestName, arguments):
    # connect
    sock = socket()
    sock.connect((host, port))

    # socket files
    outFlo = sock.makefile(mode = 'wb')
    inFlo = sock.makefile(mode = 'rb')

    # send request
    print(arguments)
    dump([requestName, arguments], outFlo)
    outFlo.flush()
    print("Sent request")

    # read response
    responseString = load(inFlo)
    print("Read response and closed socket")
    sock.close()
    return responseString
    