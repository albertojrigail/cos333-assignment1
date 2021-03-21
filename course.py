#!/usr/bin/env python

#-----------------------------------------------------------------------
# course.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------
class Course:

    def __init__(self, classId, dept, crsNum, area, title):
        self._classId = str(classId)
        self._dept = str(dept)
        self._crsNum = str(crsNum)
        self._area = str(area)
        self._title = str(title)
    
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