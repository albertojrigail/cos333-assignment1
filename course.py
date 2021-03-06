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

    def __str__(self):
        return self._classId.rjust(5) + ' ' + self._dept.rjust(4) + ' ' \
            + self._crsNum.rjust(6) + ' '  + self._area.rjust(4) + ' ' + self._title