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
    if args == "":
        arguments = [None]*4
    else:
        argv = args.split(",")
        arguments = []
        for arg in argv:
            if arg == "":
                arguments.append(None)
            else:
                arguments.append(arg)
    
    # no exception catching here
    # exceptions would be catched by regserver.py
    print("getCourse")
    print(arguments)
    db = Database()
    db.connect()
    courses = db.searchCourses(arguments)
    coursesStrings = []
    for course in courses:
        coursesStrings.append(str(course))
    db.disconnect()
    return coursesStrings
