#!/usr/bin/env python

#-----------------------------------------------------------------------
# testreg.py
# Author: Alberto Rigail
# Description: this program tests reg.py,
#              and creates the coverage report 
#-----------------------------------------------------------------------

from os import system
from sys import argv, stderr, exit

#-----------------------------------------------------------------------
def testReg(flags):
    args = "-h"
    # reference test.reg
    system("python reg.py " + args + " &>out1")
    # student test.reg
    system("python /u/cos333/Asgt1Solution/ref_reg.pyc " + args + " &>out2")
    system("diff -y out1 out2")

def main(argv):       
    testReg("-h")

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
