#!/usr/bin/env python

#-----------------------------------------------------------------------
# regserver.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import exit, argv, stderr
from os import name
from socket import socket
from socket import SOL_SOCKET, SO_REUSEADDR
from multiprocessing import Process, active_children, cpu_count
from pickle import load, dump
from time import process_time
from common import getClassDetails, getCourse
from constants import *
import argparse

# If not running on MS Windows, then import some signal-related names.
if name != 'nt':
    from signal import signal, SIGCHLD

#-----------------------------------------------------------------------

# If not running on MS Windows, then define joinChildren.  The main
# function installs it as the handler for SIGCHLD signals.
if name != 'nt':
    def joinChildren(signal, stackFrame):  
        # Wait for / reap all children that have exited.
        active_children()
    
#-----------------------------------------------------------------------

def consumeCpuTime(delay):
    
    i = 0
    initialTime = process_time()
    while (process_time() - initialTime) < delay:
        i += 1  # Do a nonsensical computation.

#-----------------------------------------------------------------------
def handleError(sock, exception):
    outFlo = sock.makefile(mode='wb')
    text = str(exception)
    textList = text.split(" ")
   
    if textList[0] == "database" or textList[0] == "file":
        dump([ERROR_CODE, DATABASE_ERROR_MESSAGE], outFlo)
    elif textList[0] == "no" and textList[1] == "such" and textList[2] == "table":
        dump([ERROR_CODE, DATABASE_ERROR_MESSAGE], outFlo)
    elif textList[0] == "no" and textList[1] == "class":
        dump([ERROR_CODE, CLASSID_ERROR_MESSAGE], outFlo)
    # I can cause this code to execute only by making the client erroneous.
    else:
        # I can cause this code to execute only by making the client erroneous.
        dump([ERROR_CODE, DATABASE_ERROR_MESSAGE], outFlo)
    outFlo.flush()

#-----------------------------------------------------------------------
def handleClient(sock, delay):
    print('Forked child process')

    try:
        inFlo = sock.makefile(mode='rb')
        incoming = load(inFlo)
        
        request = incoming[0]
        arguments = incoming[1]

        # Consume delay seconds of CPU time
        consumeCpuTime(delay)

        # call helper functions, and dump requested objects
        data = None
        if request == REQUEST_COURSES_COMMAND:
            data = getCourse(arguments)

        elif request == REQUEST_CLASS_DETAILS_COMMAND:
            data = getClassDetails(arguments)
            
        outFlo = sock.makefile(mode='wb')
        dump([SUCCESS_CODE, data], outFlo)
        outFlo.flush()

        sock.close()
        print('Closed socket in child process')
        print('Exiting child process: ')

    except Exception as e:
        handleError(sock, e)
        print(e, file=stderr)
        sock.close()
        print('Closed socket in child process')
        print('Exiting child process: ')
        exit(1)
    

 
#-----------------------------------------------------------------------

def main(argv):
    # PARSE ARGUMENTS
    parser = argparse.ArgumentParser(description="Server for the registrar application")
    parser.add_argument('port', type=int, help="the port at which the server should listen", nargs=1)
    parser.add_argument('delay', type=int, help="the seconds regserver.py should wait", nargs=1)
    arguments = parser.parse_args(argv[1:])

    # If not running on MS Windows, then install joinChildren as
    # the handler for SIGCHLD signals.
    if name != 'nt':
        signal(SIGCHLD, joinChildren)

    try:
        port = int(argv[1])
        delay = int(argv[2])

        serverSock = socket()
        serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print('Opened server socket')
        serverSock.bind(('', port))
        print('Bound server socket to port')
        serverSock.listen()
        print('Listening')
                
        while True:
            sock, address = serverSock.accept()
            print('Accepted connection, opened socket')
            
            process = Process(target=handleClient, args=[sock, delay])
            process.start()
            
            sock.close()
            print('Closed socket in parent process')
    
    # I can cause this code to execute only by making the client erroneous.
    except Exception as e:
        # I can cause this code to execute only by making the client erroneous.
        print(e, file=stderr)
        # I can cause this code to execute only by making the client erroneous.
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
