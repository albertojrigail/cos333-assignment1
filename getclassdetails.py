#!/usr/bin/env python

#-----------------------------------------------------------------------
# getclassdetails.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from database import Database
from classdetails import ClassDetails
import argparse

#-----------------------------------------------------------------------

def getClassDetails(classId):      
    # no exceptions would be caught here
    # exceptions caught in caller program (regserver.py)
    db = Database()
    db.connect()
    currentClass = db.searchClass(classId)
    db.disconnect()
    return currentClass
