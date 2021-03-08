#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from socket import socket
from pickle import load, dump
import argparse
from PyQt5.QtWidgets import QApplication, QFrame, QLabel
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QDesktopWidget, QListWidget, QScrollBar, QListWidgetItem
from PyQt5.QtCore import Qt

#-----------------------------------------------------------------------
# this function calls
def getListWidget(host, port, arguments):
    # connect
    sock = socket()
    sock.connect((host, port))

    # send request
    outFlo = sock.makefile(mode = 'wb')
    dump(["getOverviews", arguments], outFlo)

    # read response
    inFlo = sock.makefile(mode = 'rb')
    coursesStrings = load(inFlo)
    sock.close()

    # create list widget, and add courses that match
    listWidget = QListWidget()
    listWidget.addItem()
    if coursesStrings is not None:
        for courseString in coursesStrings:
            currentItem = QListWidgetItem(courseString)
            listWidget.add(currentItem)

    # set scrollbars
    verticalScrollbar = QScrollBar()
    horizontalScrollbar = QScrollBar()
    listWidget.setVerticalScrollBar(verticalScrollbar) 
    listWidget.setHorizontalScrollBar(horizontalScrollbar) 



def getDetailsPopup(host, port, classId):
    return None

def main(argv):
    # set up argparse with optional arguments
    parser = argparse.ArgumentParser(description="Client for the registrar application")
    parser.add_argument('host', type=str, help="the host on which the server is running", nargs=1)
    parser.add_argument('port', type=int, help="the port at which the server is listening", nargs=1)

    # parse arguments
    arguments = parser.parse_args(argv[1:])
    host = arguments.host[0]
    port = arguments.port[1]
    
    # graphical programming
    app = QApplication(argv)

    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)

    listWidget = getListWidget(host, port, "")
    layout.addWidget(listWidget)

    frame = QFrame()
    frame.setLayout(layout)
    
    window = QMainWindow()
    window.setWindowTitle('Princeton University Class Search')
    window.setCentralWidget(frame)
    screenSize = QDesktopWidget().screenGeometry()
    window.resize(screenSize.width()//2, screenSize.height()//2)
    
    window.show()
    exit(app.exec_())

if __name__ == '__main__':
    main(argv)
