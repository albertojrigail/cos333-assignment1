#!/usr/bin/env python

#-----------------------------------------------------------------------
# classdetails.py
# Author: Alberto Rigail
#-----------------------------------------------------------------------
import textwrap

def _strWrapper(string):
    returnString = ""
    wrapper = textwrap.TextWrapper(width=72)
    lines = wrapper.wrap(string)
    for i in range(len(lines)):
        returnString += lines[i] + "\n"
    return returnString

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

    def __str__(self):
        returnString = "Course Id: " + self._courseId + "\n\n" + \
            "Days: " + self._days + "\n" + \
            "Start time: " + self._starttime + "\n" + \
            "End time: " + self._endtime + "\n" + \
            "Building: " + self._bldg + "\n" + \
            "Room: " + self._roomnum + "\n\n"


        # dept and number
        if self._depts is not None :
            for i in range(len(self._depts)):
                returnString += _strWrapper("Dept and Number: " + self._depts[i])
        
        returnString += "\n"
        returnString += "Area: " + self._area + "\n\n"
        
        # title
        returnString += _strWrapper("Title: " + self._title)
        returnString += "\n"
        
        # description
        returnString += _strWrapper("Description: " + self._descrip)
        returnString += "\n"
        # prereqs
        returnString += _strWrapper("Prerequisites: " + self._prereqs)
        returnString += "\n"
        
        #professors
        if self._profs is not None :
            for i in range(len(self._profs)):
                returnString += _strWrapper("Professor: " + self._profs[i])
        return returnString