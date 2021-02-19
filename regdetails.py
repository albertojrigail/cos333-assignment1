#!/usr/bin/env python

#-----------------------------------------------------------------------
# regdetails.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect
import argparse
import textwrap 

#-----------------------------------------------------------------------
def listToString(list):
    string = ""
    if len(list) == 0:
        return ""
    if len(list) == 1:
        return list[0]
    else:
        string += list[0]
        for i in range(1, len(list)):
            if i == len(list) - 1:
                string += " and " + list[i]
            else:
                string += ", " + list[i]

def printWrapped(string):
    wrapper = textwrap.TextWrapper(width=72)
    lines = wrapper.wrap(string)
    for i in range(len(lines)):
        print(lines[i])

def main(argv):       
    
    DATABASE_NAME = 'reg.sqlite'

    # set up argparse with optional arguments
    parser = argparse.ArgumentParser(description="Registrar application: show details about a class")
    parser.add_argument('classid', type=int, help="the id of the class whose details should be shown")

    # parse arguments
    arguments = parser.parse_args(argv[1:])
    classid = arguments.classid

    # check if database is in current directory
    if not path.isfile(DATABASE_NAME):
       print('Database connection failed', file=stderr)
       exit(1)       
    try:
        connection = connect(DATABASE_NAME)
        cursor = connection.cursor()

        # create a prepared statement and substitute values.
        stmtStr = 'SELECT classes.courseid, days, starttime, endtime, bldg, roomnum, area, title, descrip, prereqs ' + \
            'FROM classes, courses WHERE classes.courseid = courses.courseid AND classes.classid = ?'
        cursor.execute(stmtStr, [classid])
        
        # get all fields except profname, and departments
        row = cursor.fetchone()
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
        stmStr = 'SELECT dept, coursenum FROM crosslistings WHERE courseid = ?'
        cursor.execute(stmStr, [courseid])
        depts = []
        row = cursor.fetchone()
        while row is not None:
            current = row[0] + ' ' + row[1]
            depts.append(current)
            row = cursor.fetchone()

        # get profname
        stmStr = 'SELECT profname FROM coursesprofs, profs ' + \
            'WHERE coursesprofs.profid = profs.profid AND courseid = ?'
        cursor.execute(stmtStr, [courseid])
        profs = []
        row = cursor.fetchone()
        print(row)
        while row is not None:
            current = row[0]
            profs.append(current)
            row = cursor.fetchone()
         
        # format print statements
        print("Course Id:", courseid, end="\n\n")
        print("Days:", days)
        print("Start time:", starttime)
        print("End time:", endtime)
        print("Building:", bldg)
        print("Room:", roomnum, end="\n\n")

        # dept and number
        dptnum = "Dept and Number: " + listToString(depts)
        printWrapped(dptnum)
        print("")

        # Area
        print("Area:", area, end="\n\n")

        # title
        printWrapped("Title: " + title)
        print("")

        # Description
        printWrapped("Description: " + descrip)
        print("")

        # prereqs
        printWrapped("Prerequisites: " + prereqs)
        print("")

        # professors
        profsStr = "Professor: " + listToString(profs)
        printWrapped(profsStr)
        
        # finish (good practice)
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(e, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
