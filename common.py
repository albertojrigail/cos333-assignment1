#!/usr/bin/env python

#-----------------------------------------------------------------------
# common.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from database import Database

#-----------------------------------------------------------------------
def getClassDetails(classId):      
    # no exceptions would be caught here
    # exceptions caught in caller program (regserver.py)
    db = Database()
    db.connect()
    currentClass = db.searchClass(classId)
    db.disconnect()
    return str(currentClass)

#-----------------------------------------------------------------------
def getCourse(args):       
    # parse arguments
    argv = args.split(",")
    arguments = []
    for arg in argv:
        if arg == "":
            arguments.append(None)
        else:
            arguments.append(arg)

    # no exception catching here
    # exceptions would be catched by regserver.py
    db = Database()
    db.connect()
    courses = db.searchCourses(arguments)
    coursesStrings = []
    for course in courses:
        coursesStrings.append(str(course))
    db.disconnect()
    return coursesStrings

