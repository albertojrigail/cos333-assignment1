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
    system("python regdetails.py " + courseid + " &>out3")
    # student test.reg
    system("python /u/cos333/Asgt1Solution/ref_regdetails.pyc " + courseid + " &>out4")
    system("diff out3 out4")
    system("rm -rf out3 out4")

def main(argv):
    DATABASE_NAME = 'reg.sqlite'

    # check if database is in current directory
    if not path.isfile(DATABASE_NAME):
       print('Database connection failed', file=stderr)
       exit(1)
    try:
        connection = connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT classid from classes ORDER BY classid")

        row = cursor.fetchone()
        while row is not None:
            print("test:", str(row[0]))
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
