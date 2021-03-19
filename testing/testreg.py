#!/usr/bin/env python
#-----------------------------------------------------------------------
# testreg.py
# Author: Alberto Rigail
# Description: this program tests reg.py,
#-----------------------------------------------------------------------

from os import system
from sys import argv, stderr, exit

#-----------------------------------------------------------------------
def testReg(flags):
    print("Test flags: " + flags)
    # reference test.reg
    system("python reg.py " + flags + " &>out1")
    # student test.reg
    system("python /u/cos333/Asgt1Solution/ref_reg.pyc " + flags + " &>out2")
    system("diff out1 out2")
    system("rm -rf out1 out2")
    print("")

def main(argv):
    # standard tests       
    testReg("-h")
    testReg("python reg.py")
    testReg("-d COS")
    testReg("-n 333")
    testReg("-n b")
    testReg("-a Qr")
    testReg("-t intro")
    testReg("-t science")
    testReg("-t C_S")
    testReg("-t c%S")
    testReg("-d cos -n 3")
    testReg("-d cos -a qr -n 2 -t intro")
    testReg("-t 'Independent Study'")
    testReg("-t 'Independent Study '")
    testReg("-t 'Independent Study  '")
    testReg("-t ' Independent Study'")
    testReg("-t '  Independent Study'")
    testReg("-t=-c")

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
