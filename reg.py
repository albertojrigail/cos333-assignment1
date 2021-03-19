#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from request import sendRequest
import argparse
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout,QHBoxLayout, QDesktopWidget, QListWidget, QScrollBar, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QBrush

#-----------------------------------------------------------------------

REQUEST_COURSES_COMMAND = "getOverviews"
REQUEST_CLASS_DETAILS_COMMAND = "getDetail"

#-----------------------------------------------------------------------

# this function makes a list widget, amnd calls 
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
    screenSize = QDesktopWidget().screenGeometry()

    # CREATE LIST WITH COURSES
    listWidget = QListWidget()
    font = QFont('Courier', 10) 
    verticalScrollbar = QScrollBar()
    horizontalScrollbar = QScrollBar()
    listWidget.setVerticalScrollBar(verticalScrollbar) 
    listWidget.setHorizontalScrollBar(horizontalScrollbar) 
    listWidget.setItemAlignment(Qt.AlignLeft)
    listWidget.resize(screenSize.width()//2, screenSize.height()//4)

    # on double click, show class details
    def ItemDobleClicked():
        item = listWidget.currentItem()
        text = str(item.text())
        row = text.split(' ')
        classId = row[1] # location of the classId string
        try:
            classDetails = sendRequest(host, port, REQUEST_CLASS_DETAILS_COMMAND, classId)
        except Exception as e:
            reply = QMessageBox.critical(window, "Error", str(e))
        else:
            # message box formatting and return
            reply = QMessageBox.information(window, "Class Details", classDetails)
    listWidget.itemActivated.connect(ItemDobleClicked)

    # fill the list with courses that match with "arguments"
    def updateList(arguments):
        listWidget.clear()
        try:
            courses = sendRequest(host, port, REQUEST_COURSES_COMMAND, arguments)
        except Exception as e:
            reply = QMessageBox.critical(window, "Error", str(e))
        else:
            if courses is not None:
                for course in courses:
                    currentItem = QListWidgetItem(course)
                    currentItem.setFont(font)
                    listWidget.addItem(currentItem)      

    # CREATE TOP FORM WITH INPUT FIELDS AND BUTTON
    formWidgetLayout = QHBoxLayout()
    fieldsLayout = QFormLayout()
    fieldsLayout.setLabelAlignment(Qt.AlignRight)
    formWidgetLayout.setSpacing(0)
    fieldsLayout.setSpacing(0)
    formWidgetLayout.setContentsMargins(0, 0, 0, 0)
    fieldsLayout.setContentsMargins(0, 0, 0, 0)


    deptEdit = QLineEdit()    
    numEdit = QLineEdit()
    areaEdit = QLineEdit()
    titleEdit = QLineEdit()
    
    deptLabel = QLabel("Dept:")
    numLabel = QLabel("Number:")
    areaLabel = QLabel("Area:")
    titleLabel = QLabel("Title:")

    fieldsLayout.addRow(deptLabel, deptEdit)
    fieldsLayout.addRow(numLabel, numEdit)
    fieldsLayout.addRow(areaLabel, areaEdit)
    fieldsLayout.addRow(titleLabel, titleEdit)

    fieldFrame = QFrame()
    fieldFrame.setLayout(fieldsLayout)
    submitButton = QPushButton("Submit")
    formWidgetLayout.addWidget(fieldFrame)
    formWidgetLayout.addWidget(submitButton)
    formWidgetFrame = QFrame()
    formWidgetFrame.setLayout(formWidgetLayout)
    formWidgetFrame.resize(screenSize.width()//2, screenSize.height()//4)

    # set up submitting logic
    def submitQuery():
        dept = deptEdit.text()
        num = numEdit.text()
        area = areaEdit.text()
        title = titleEdit.text()
        arguments = dept + "," + num + "," + area + "," + title
        # set up arguments
        args = arguments.strip()
        updateList(args)
    submitButton.clicked.connect(submitQuery)
    submitButton.setAutoDefault(True)
    deptEdit.returnPressed.connect(submitQuery)
    numEdit.returnPressed.connect(submitQuery)
    areaEdit.returnPressed.connect(submitQuery)
    titleEdit.returnPressed.connect(submitQuery)


    # ADD FORM AND LIST TO LAYOUT
    layout.addWidget(formWidgetFrame)
    layout.addWidget(listWidget)

    # GENERAL WINDOW SETUP
    frame = QFrame()
    frame.setLayout(layout)
    window = QMainWindow()
    window.setWindowTitle('Princeton University Class Search')
    window.setCentralWidget(frame)
    window.resize(screenSize.width()//2, screenSize.height()//2)
    window.show()


    # GET COURSES
    #initial call
    updateList("")  

    exit(app.exec_())

if __name__ == '__main__':
    main(argv)
