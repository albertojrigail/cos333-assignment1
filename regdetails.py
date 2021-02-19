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
            'WHERE coursesprofs.profid = profs.profid AND coursesprofs.courseid = ?'
        cursor.execute(stmtStr, [courseid])
        profs = []
        row = cursor.fetchone()
        while row is not None:
            profs.append(row[0])
            row = cursor.fetchone()
        
        # format print statements
        print("Course Id:", courseid, end="\n\n")
        print("Days:", days)
        print("Start time:", starttime)
        print("End time:", endtime)
        print("Building:", bldg)
        print("Room:", roomnum, end="\n\n")

        # dept and number
        print("Dept and Number:", end="")
        print(" ", depts[0])
        for i in range(1, len(depts)):
            if i == len(depts) - 1:
                print(" and ", depts[i], end="")
            else:
                print(", ", depts[i], end="")
        print("")

        # Area
        print("Area:", area, end="\n\n")

        # title
        wrapper = textwrap.TextWrapper(width=72)
        title = "Title: " + title
        titleLines = wrapper.wrap(title)
        for i in range(len(titleLines)):
            print(titleLines[i])

        # Description
        descrip = "Description: " + descrip
        descripLines = wrapper.wrap(descrip)
        for i in range(len(descripLines)):
            print(descripLines[i])

        # prereqs
        print("Prerequisites:", prereqs, end="\n\n")

        # professors
        print("Professor:", end="")
        print(" ", profs[0])
        for i in range(1, len(profs)):
            if i == len(profs) - 1:
                print(" and ", profs[i], end="")
            else:
                print(", ", profs[i], end="")
        print("")
        
        # finish (good practice)
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(e, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
