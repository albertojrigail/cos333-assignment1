#!/usr/bin/env python

#-----------------------------------------------------------------------
# getcourse.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from database import Database
from course import Course
import argparse

#-----------------------------------------------------------------------

def getCourse(args):       
    # parse arguments
    arguments = []
    for arg in args:
        if arg is not None and arg != "":
            arguments.append(arg)
        else:
            arguments.append(None)
    
    db = Database()
    db.connect()
    courses = db.searchCourses(arguments)
    db.disconnect()
    return courses
