#!/usr/bin/env python

#-----------------------------------------------------------------------
# classdetails.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------
class ClassDetails:

    def __init__(self, courseId, days, starttime, endtime, \
                bldg, roomnum, area, title, descrip, prereqs, depts, profs):
        self._courseId = str(courseId)
        self._days = str(days)
        self._starttime = str(starttime)
        self._endtime = str(endtime)
        self._bldg = str(bldg)
        self._roomnum = str(roomnum)
        self._area = str(area)
        self._title = str(title)
        self._descrip = str(descrip)
        self._prereqs = str(prereqs)
        self._depts = depts
        self._profs = profs
    
    def getCourseId(self):
        return self._courseId
    
    def getDays(self):
        return self._days
    
    def getStartTime(self):
        return self._starttime
    
    def getEndTime(self):
        return self._endtime
    
    def getBldg(self):
        return self._bldg
    
    def getRoomnum(self):
        return self._roomnum
    
    def getArea(self):
        return self._area
    
    def getTitle(self):
        return self._title
    
    def getDescrip(self):
        return self._descrip
    
    def getPrereqs(self):
        return self._prereqs
    
    def getDepts(self):
        return self._depts
    
    def getProfs(self):
        return self._profs