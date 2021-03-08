#!/usr/bin/env python

#-----------------------------------------------------------------------
# getcourse.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------

from sys import argv, stderr, exit
from database import Database
import argparse

#-----------------------------------------------------------------------

def getCourse(args):       
    # set up argparse with optional arguments
    parser = argparse.ArgumentParser(description="Registrar application: show overviews of classes", allow_abbrev=False)
    parser.add_argument('-d', metavar='dept', type=str, help="show only those classes whose department contains dept", nargs=1)
    parser.add_argument('-n', metavar='num', type=str, help="show only those classes whose course number contains num", nargs=1)
    parser.add_argument('-a', metavar='area', type=str, help="show only those classes whose distrib area contains area", nargs=1)
    parser.add_argument('-t', metavar='title', type=str, help="show only those classes whose course title contains title", nargs=1)
    
    # parse arguments
    arguments = parser.parse_args(args)
    arguments = [arguments.d, arguments.n, arguments.a, arguments.t]

    # no exception catching here
    # exceptions would be catched by regserver.py
    db = Database()
    db.connect()
    courses = db.searchCourses(arguments)
    db.disconnect()
    return courses