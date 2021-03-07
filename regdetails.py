#!/usr/bin/env python

#-----------------------------------------------------------------------
# regdetails.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from database import Database
import argparse

#-----------------------------------------------------------------------

def main(argv):  
    DATABASE_NAME = 'reg.sqlite'

    # set up argparse with optional arguments
    parser = argparse.ArgumentParser(description="Registrar application: show details about a class")
    parser.add_argument('classid', type=int, help="the id of the class whose details should be shown", nargs=1)

    # parse arguments
    arguments = parser.parse_args(argv[1:])
    classId = arguments.classid[0]
    print(classId)

    try:
        db = Database()
        db.connect()
        currentClass = db.searchClass(classId)
        print("getting current class successful!")
        print(currentClass)
        db.disconnect

    except Exception as e:
        print(argv[0] + ':', e, file=stderr)
        exit(1)   

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
