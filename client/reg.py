#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from request import sendRequest
import argparse
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton
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
    listWidgetFrame = QFrame()
    listWidgetFrame.setLayout(listWidget)
    

    # on double click, show class details
    def ItemDobleClicked():
        item = listWidget.currentItem()
        text = str(item.text())
        row = text.split(' ')
        classId = row[1] # location of the classId string
        classDetails = sendRequest(host, port, REQUEST_CLASS_DETAILS_COMMAND, classId)

        # message box formatting and return
        reply = QMessageBox.information(window, "Class Information", classDetails)
    listWidget.itemDoubleClicked.connect(ItemDobleClicked)

    # fill the list with courses that match with "arguments"
    def updateList(arguments):
        listWidget.clear()
        courses = sendRequest(host, port, REQUEST_COURSES_COMMAND, arguments)
        if courses is not None:
            for course in courses:
                currentItem = QListWidgetItem(course)
                currentItem.setFont(font)
                listWidget.addItem(currentItem)
        
    # CREATE TOP FORM WITH INPUT FIELDS AND BUTTON
    formWidgetLayout = QVBoxLayout()
    classIdEdit = QLineEdit()
    deptEdit = QLineEdit()
    noEdit = QLineEdit()
    areaEdit = QLineEdit()
    titleEdit = QLineEdit()
    submitButton = QPushButton()

    formWidgetLayout.addWidget(classIdEdit)
    formWidgetLayout.addWidget(deptEdit)
    formWidgetLayout.addWidget(noEdit)
    formWidgetLayout.addWidget(areaEdit)
    formWidgetLayout.addWidget(titleEdit)
    formWidgetLayout.addWidget(submitButton)
    formWidgetFrame = QFrame()
    formWidgetFrame.setLayout(formWidgetLayout)

    # set up submitting logic
    def submitQuery():
        arguments = ""
        # set up arguments
        updateList(arguments)
    submitButton.clicked.connect(submitQuery)


    # ADD FORM AND LIST TO LAYOUT
    layout.addWidget(formWidgetFrame)
    layout.addWidget(listWidgetFrame)

    # GENERAL WINDOW SETUP
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
