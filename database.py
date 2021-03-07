#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sqlite3 import connect
from sys import stderr
from os import path
from course import Course
from classdetails import ClassDetails

#-----------------------------------------------------------------------

class Database:
    
    def __init__(self):
        self._connection = None

    def connect(self):      
        DATABASE_NAME = 'reg.sqlite'
        if not path.isfile(DATABASE_NAME):
            raise Exception('database reg.sqlite not found')
        self._connection = connect(DATABASE_NAME)
                    
    def disconnect(self):
        self._connection.close()

    def searchCourses(self, arguments):
        dept = arguments[0]
        num = arguments[1]
        area = arguments[2]
        title = arguments[3]

        # create a prepared statement and substitute values.
        stmtStr = 'SELECT classid, dept, coursenum, area, title ' + \
            'FROM classes, courses, crosslistings ' + \
            'WHERE classes.courseid = courses.courseid ' + \
            'AND courses.courseid = crosslistings.courseid'
        
        # add specific conditions given by optional arguments
        optionalArguments = []
        if(dept is not None):
            stmtStr = stmtStr + ' AND INSTR(LOWER(crosslistings.dept), ?)'
            optionalArguments.append(str.lower(dept[0]))
        if(num is not None):
            stmtStr = stmtStr + ' AND INSTR(LOWER(crosslistings.coursenum), ?)'
            optionalArguments.append(num[0])
        if(area is not None):
            stmtStr = stmtStr + ' AND INSTR(LOWER(courses.area), ?)'
            optionalArguments.append(str.lower(area[0]))
        if(title is not None):
            stmtStr = stmtStr + ' AND INSTR(LOWER(courses.title), ?)'
            optionalArguments.append(str.lower(title[0]))
        stmtStr = stmtStr + ' ORDER BY dept, coursenum, classid'

        # execute statement
        cursor = self._connection.cursor()
        if(dept or num or area or title):
            cursor.execute(stmtStr, optionalArguments)
        else:
            cursor.execute(stmtStr)

        # return list of course objects
        courses = []
        row = cursor.fetchone()
        while row is not None:
            # fields
            course = Course(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
            courses.append(course)
            # next entry
            row = cursor.fetchone()
        cursor.close()
        return courses
    
    def searchClass(self, classId):
        # create a prepared statement and substitute values.
        stmtStr = 'SELECT classes.courseid, days, starttime, endtime, bldg, roomnum, area, title, descrip, prereqs ' + \
            'FROM classes, courses WHERE classes.courseid = courses.courseid AND classes.classid = ?'
        
        # execute statement
        cursor = self._connection.cursor()
        cursor.execute(stmtStr, [classId])
        
        # get all fields except profname, and departments
        row = cursor.fetchone()
        if row is None:
            raise Exception("no class with classid " + classId + " exists")

        courseid = str(row[0])
        days = str(row[1])
        starttime = str(row[2])
        endtime = str(row[3])
        bldg = str(row[4])
        roomnum = str(row[5])
        area = str(row[6])
        title = str(row[7])
        descrip = str(row[8])
        prereqs = str(row[9])

        # get departments and coursenums
        stmtStr = 'SELECT dept, coursenum FROM crosslistings WHERE courseid = ? ' + \
                    'ORDER BY dept, coursenum'
        cursor.execute(stmtStr, [courseid])
        depts = []
        row = cursor.fetchone()
        while row is not None:
            current = row[0] + ' ' + row[1]
            depts.append(current)
            row = cursor.fetchone()

        # get profname
        stmtStr = 'SELECT profname FROM coursesprofs, profs ' + \
            'WHERE coursesprofs.profid = profs.profid AND courseid = ? ' +\
                "ORDER BY profname"
        cursor.execute(stmtStr, [courseid])
        profs = []
        row = cursor.fetchone()
        while row is not None:
            current = row[0]
            profs.append(current)
            row = cursor.fetchone()

        # create object
        return ClassDetails(courseid, days, starttime, endtime, bldg, roomnum, \
            area, title, descrip, prereqs, depts, profs)

#----------------------------------=-------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    courses = database.searchCourses('courses', [None, None, None, None])
    for course in courses:
        print(course)
    database.disconnect()