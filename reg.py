#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from database import Database
import argparse

#-----------------------------------------------------------------------

def main(argv):       
    
    DATABASE_NAME = 'reg.sqlite'

    # set up argparse with optional arguments
    parser = argparse.ArgumentParser(description="Registrar application: show overviews of classes", allow_abbrev=False)
    parser.add_argument('-d', metavar='dept', type=str, help="show only those classes whose department contains dept", nargs=1)
    parser.add_argument('-n', metavar='num', type=str, help="show only those classes whose course number contains num", nargs=1)
    parser.add_argument('-a', metavar='area', type=str, help="show only those classes whose distrib area contains area", nargs=1)
    parser.add_argument('-t', metavar='title', type=str, help="show only those classes whose course title contains title", nargs=1)
    
    # parse arguments
    arguments = parser.parse_args()
    arguments = [arguments.d, arguments.n, arguments.a, arguments.t]

    try:
        db = Database()
        db.connect()
        courses = db.searchCourses(arguments)
        # format print statements
        print("ClsId Dept CrsNum Area Title")
        print("----- ---- ------ ---- -----")

        for course in courses:
            print(course, end="")

        db.disconnect()

    except Exception as e:
        print(argv[0] + ':', e, file=stderr)
        exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
