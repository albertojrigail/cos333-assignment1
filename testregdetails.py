#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregdetails.py
# Author: Alberto Rigail
# Description: this program tests regdetails.py,
#-----------------------------------------------------------------------

from os import system, path
from sys import argv, stderr, exit
from sqlite3 import connect

#-----------------------------------------------------------------------
def testRegDetails(courseid):
    # reference test.reg
    system("python testreg.py " + courseid + " &>out1")
    # student test.reg
    system("python /u/cos333/Asgt1Solution/ref_testreg.pyc " + courseid + " &>out2")
    system("diff out1 out2")
    system("rm -rf out1 out2")

def main(argv):
    DATABASE_NAME = 'reg.sqlite'

    # check if database is in current directory
    if not path.isfile(DATABASE_NAME):
       print('Database connection failed', file=stderr)
       exit(1)
    try:
        connection = connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT classid from classes")

        row = cursor.fetchone()
        while row is not None:
            testRegDetails(str(row[0]))
            row = cursor.fetchone()

        # finish (good practice)
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=stderr)
        exit(1)


    # test all classes
    testRegDetails()

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
