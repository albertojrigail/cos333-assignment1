#!/usr/bin/env python

#-----------------------------------------------------------------------
# course.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------
import textwrap

class Course:

    def __init__(self, classId, dept, crsNum, area, title):
        self._classId = str(classId)
        self._dept = str(dept)
        self._crsNum = str(crsNum)
        self._area = str(area)
        self._title = str(title)

    def __str__(self):
        courseString = self._classId.rjust(5) + ' ' + self._dept.rjust(4) + ' ' \
            + self._crsNum.rjust(6) + ' '  + self._area.rjust(4)
        
        # format title so that it appears in different lines
        wrapper = textwrap.TextWrapper(width=49)
        titleLines = wrapper.wrap(self._title)
        courseString += titleLines[0] + "\n"
        for i in range(1, len(titleLines)):
            courseString += '                       ' + titleLines[i] + "\n"
        return courseString
        
    def getClassId(self):
        return self._classId

    def getDept(self):
        return self._dept
    
    def getCrsNum(self):
        return self._crsNum
    
    def getArea(self):
        return self._area

    def getTitle(self):
        return self._title