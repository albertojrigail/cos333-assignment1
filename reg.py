#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
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
    parser = argparse.ArgumentParser(description="Registrar application: show overviews of classes", allow_abbrev=False)
    parser.add_argument('-d', metavar='dept', type=str, help="show only those classes whose department contains dept", nargs=1)
    parser.add_argument('-n', metavar='num', type=str, help="show only those classes whose course number contains num", nargs=1)
    parser.add_argument('-a', metavar='area', type=str, help="show only those classes whose distrib area contains area", nargs=1)
    parser.add_argument('-t', metavar='title', type=str, help="show only those classes whose course title contains title", nargs=1)
    
    # text wrapper
    formattedArguments = []
    for i in range(1, len(argv)):
        # only remove whitespace if argument is -option (odd)
        if i%2 == 0:
            formattedArguments.append(argv[i].strip())
        else:
            formattedArguments.append(argv[i])

    # parse arguments
    arguments = parser.parse_args(formattedArguments)
    dept = arguments.d
    num = arguments.n
    area = arguments.a
    title = arguments.t

    # check if database is in current directory
    if not path.isfile(DATABASE_NAME):
       print(argv[0], ': database reg.sqlite not found', file=stderr)
       exit(1)       
    try:
        connection = connect(DATABASE_NAME)
        cursor = connection.cursor()

        # create a prepared statement and substitute values.
        stmtStr = 'SELECT classid, dept, coursenum, area, title ' + \
            'FROM classes, courses, crosslistings ' + \
            'WHERE classes.courseid = courses.courseid ' + \
            'AND courses.courseid = crosslistings.courseid'
        
        # add specific conditions given by optional arguments
        optionalArguments = []
        if(dept is not None):
            stmtStr = stmtStr + ' AND INSTR(LOWER(crosslistings.dept), ?)'
            optionalArguments.append(str.lower(dept))
        if(num is not None):
            stmtStr = stmtStr + ' AND INSTR(LOWER(crosslistings.coursenum), ?)'
            optionalArguments.append(num)
        if(area is not None):
            stmtStr = stmtStr + ' AND INSTR(LOWER(courses.area), ?)'
            optionalArguments.append(str.lower(area))
        if(title is not None):
            stmtStr = stmtStr + ' AND INSTR(LOWER(courses.title), ?)'
            optionalArguments.append(str.lower(title))
        stmtStr = stmtStr + ' ORDER BY dept, coursenum, classid'
        
        # execute statement
        if(dept or num or area or title):
            cursor.execute(stmtStr, optionalArguments)
        else:
            cursor.execute(stmtStr)

        # format print statements
        print("ClsId Dept CrsNum Area Title")
        print("----- ---- ------ ---- -----")
        wrapper = textwrap.TextWrapper(width=49)

        row = cursor.fetchone()
        while row is not None:
            # fields
            ClsId = str(row[0])
            Dept = str(row[1])
            CrsNum = str(row[2])
            Area = str(row[3])
            Title = str(row[4])

            print(ClsId.rjust(5), Dept.rjust(4), CrsNum.rjust(6), Area.rjust(4), end=' ')
            
            # format title so that it appears in different lines
            titleLines = wrapper.wrap(Title)
            print(titleLines[0])
            for i in range(1, len(titleLines)):
                print('                       ', end='')
                print(titleLines[i])

            # next entry
            row = cursor.fetchone()

        # finish (good practice)
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(argv[0] + ':', e, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
