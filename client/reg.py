#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from request import sendRequest
import argparse
from PyQt5.QtWidgets import QApplication, QFrame, QLabel
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QDesktopWidget, QListWidget, QScrollBar, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

#-----------------------------------------------------------------------

REQUEST_COURSES_COMMAND = "getOverviews"
REQUEST_CLASS_DETAILS_COMMAND = "getDetail"

#-----------------------------------------------------------------------

# this function makes a list widget, amnd calls 


def getDetailsPopup(host, port, classId):
    return None

def main(argv):
    # PARSE ARGUMENTS
    parser = argparse.ArgumentParser(description="Client for the registrar application")
    parser.add_argument('host', type=str, help="the host on which the server is running", nargs=1)
    parser.add_argument('port', type=int, help="the port at which the server is listening", nargs=1)
    arguments = parser.parse_args(argv[1:])
    host = arguments.host[0]
    port = arguments.port[0]
    
    # CREATE INITIAL INTERFACE
    app = QApplication(argv)
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)


    # CREATE LIST WITH COURSES
    listWidget = QListWidget()
    font = QFont('Courier', 10) 
    verticalScrollbar = QScrollBar()
    horizontalScrollbar = QScrollBar()
    listWidget.setVerticalScrollBar(verticalScrollbar) 
    listWidget.setHorizontalScrollBar(horizontalScrollbar) 
    listWidget.setItemAlignment(Qt.AlignLeft)

    # on double click, show class details
    def ItemDobleClicked():
        print("ItemDoubleClicked")
        item = listWidget.currentItem()
        text = str(item.text())
        row = text.split(' ')
        classId = row[1] # location of the classId string
        classDetails = sendRequest(host, port, REQUEST_CLASS_DETAILS_COMMAND, classId)
        reply = QMessageBox.information(window, "Class Information", classDetails)
        reply.setFont(font)

   # fill up list with courses
    listWidget.itemDoubleClicked.connect(ItemDobleClicked)
    courses = sendRequest(host, port, REQUEST_COURSES_COMMAND, "")
    if courses is not None:
        for course in courses:
            currentItem = QListWidgetItem(course)
            currentItem.setFont(font)
            listWidget.addItem(currentItem)


    # add list widget to layout
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
