#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
import argparse
from threading import Thread
from socket import socket
from pickle import load, dump
from PyQt5.QtWidgets import QApplication, QFrame, QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton, QFormLayout
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QDesktopWidget
from PyQt5.QtWidgets import QListWidget, QScrollBar, QListWidgetItem, QMessageBox
from queue import Queue
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from constants import *

workerThread = None

#-----------------------------------------------------------------------
def request(host, port, requestName, arguments):
    sock = socket()
    sock.connect((host, port))

    # Send request      
    outFlo = sock.makefile(mode='wb')
    dump([requestName, arguments], outFlo)
    outFlo.flush()
    print("Sent command:", requestName)

    # Read response
    inFlo = sock.makefile(mode='rb')
    responseData = load(inFlo)
    code = responseData[0]
    data = responseData[1]
    sock.close()

    # return values
    return code, data

#-----------------------------------------------------------------------
class WorkerThread (Thread):

    def __init__(self, host, port, requestName, arguments, queue):
        Thread.__init__(self)
        self._host = host
        self._port = port
        self._requestName = requestName 
        self._arguments = arguments
        self._queue = queue
        self._shouldStop = False

    def stop(self):
        self._shouldStop = True
    
    def run(self):
        try:
            code, data = request(self._host, self._port, self._requestName, self._arguments)
            if code != 200:
                raise Exception(data)
            if self._shouldStop:
                return
            self._queue.put([True, self._requestName, data])
        except Exception as e:
            if self._shouldStop:
                return
            self._queue.put([False, self._requestName, str(e)])

    
#-----------------------------------------------------------------------

def main(argv):
    # PARSE ARGUMENTS
    parser = argparse.ArgumentParser(description="Client for the registrar application")
    parser.add_argument('host', type=str, help="the host on which the server is running", nargs=1)
    parser.add_argument('port', type=int, help="the port at which the server is listening", nargs=1)
    arguments = parser.parse_args(argv[1:])
    host = arguments.host[0]
    port = int(arguments.port[0])

    queue = Queue()
    
    # Create and lay out the widgets

    app = QApplication(argv)
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    screenSize = QDesktopWidget().screenGeometry()

    listWidget = QListWidget()
    font = QFont('Courier', 10) 
    verticalScrollbar = QScrollBar()
    horizontalScrollbar = QScrollBar()
    listWidget.setVerticalScrollBar(verticalScrollbar) 
    listWidget.setHorizontalScrollBar(horizontalScrollbar) 
    listWidget.setItemAlignment(Qt.AlignLeft)
    listWidget.resize(screenSize.width()//2, screenSize.height()//4)

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
    formWidgetLayout.addWidget(fieldFrame)
    formWidgetFrame = QFrame()
    formWidgetFrame.setLayout(formWidgetLayout)
    formWidgetFrame.resize(screenSize.width()//2, screenSize.height()//4)
    
    layout.addWidget(formWidgetFrame)
    layout.addWidget(listWidget)

    frame = QFrame()
    frame.setLayout(layout)
    window = QMainWindow()
    window.setWindowTitle('Princeton University Class Search')
    window.setCentralWidget(frame)
    window.resize(screenSize.width()//2, screenSize.height()//2)

    # Handle signals

    # on double click, show class details
    def ItemDobleClicked():
        try:
            item = listWidget.currentItem()
            text = str(item.text())
            row = text.split(' ')
            classId = row[1]
            code, data = request(host, port, REQUEST_CLASS_DETAILS_COMMAND, classId)
            if code != 200:
                raise Exception(data)

            # for getClassDetails, show popup window with text
            if data is not None:
                classDetails = data
                return QMessageBox.information(window, "Class Details", classDetails)
                
        except Exception as e:
            return QMessageBox.critical(window, "Error", str(e))

    listWidget.itemActivated.connect(ItemDobleClicked)


    def submitSlot():
        global workerThread
        dept = deptEdit.text()
        num = numEdit.text()
        area = areaEdit.text()
        title = titleEdit.text()
        arguments = dept + "," + num + "," + area + "," + title
        args = arguments.strip()

        if workerThread is not None:
            workerThread.stop()
        workerThread = WorkerThread(host, port, REQUEST_COURSES_COMMAND, args, queue)
        workerThread.start()

    deptEdit.textChanged.connect(submitSlot)
    numEdit.textChanged.connect(submitSlot)
    areaEdit.textChanged.connect(submitSlot)
    titleEdit.textChanged.connect(submitSlot)
    
    #-------------------------------------------------------------------
    # Create a timer that polls the queue.

    def pollQueue():
        # read responses and render events properly
        while not queue.empty():
            response = queue.get()
            successful = response[0]
            requestName = response[1]
            data = response[2]

            # for error, show popup window with message
            if successful is not True:
                return QMessageBox.critical(window, "Error", data)


            # for getCourse, clear list and show results
            if requestName == REQUEST_COURSES_COMMAND:
                if data is not None:
                    listWidget.clear()

                    courses = data
                    for course in courses:
                        currentItem = QListWidgetItem(course)
                        currentItem.setFont(font)
                        listWidget.addItem(currentItem)   
                    
                    listWidget.repaint()


    timer = QTimer()
    timer.timeout.connect(pollQueue)
    timer.setInterval(100) # milliseconds
    timer.start()
    #-------------------------------------------------------------------

    window.show()

    submitSlot()  # Populate list of courses initially.

    # Start the event loop.
    exit(app.exec_())

if __name__ == '__main__':
    main(argv)
