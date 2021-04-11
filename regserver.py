#!/usr/bin/env python

#-----------------------------------------------------------------------
# regserver.py
# Author: Bob Dondero
#-----------------------------------------------------------------------
from sys import exit, argv, stderr
from database import Database
from constants import *

#Flask-specific imports
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template

#-----------------------------------------------------------------------
app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    dept = request.args.get('dept')
    num = request.args.get('num')
    area = request.args.get('area')
    title = request.args.get('title')
    arguments = [dept, num, area, title]

    isError = False
    errorMsg = ""

    # database
    courses=None
    try:
        db = Database()
        db.connect()
        courses = db.searchCourses(arguments)
        db.disconnect()

    except Exception as e:
        isError = True
        error = str(e)
        # no class id exists
        errorMsg = "A server error occurred. Please contact the system administrator."
        if error == 'database reg.sqlite not found':
            print('runserver.py: database reg.sqlite not found', file=stderr)
        else:
            print('runserver.py: ' + error, file=stderr)

    if dept is None:
        dept = ""
    if num is None:
        num = ""
    if area is None:
        area = ""
    if title is None:
        title =""
    # pass the arguments to jinja2
    html = render_template('templates/index.html',
        courses=courses,
        dept=dept,
        num=num,
        area=area,
        title=title,
        isError=isError,
        errorMsg=errorMsg,
    )
    response = make_response(html)
    response.set_cookie('prevDept', dept)
    response.set_cookie('prevNum', num)
    response.set_cookie('prevArea', area)
    response.set_cookie('prevTitle', title)
    return response
    
#-----------------------------------------------------------------------

@app.route('/regdetails', methods=['GET'])
def regdetails():
    classId = request.args.get('classid')
    classDetails = None
    isError = False
    errorMsg = ""

    # error handling
    # missing classId
    if classId is None or classId == "":
        isError = True
        errorMsg = "missing classid"

    if isError == False:
        # non integer classId
        try:
            classId = int(classId)

        except:
            isError = True
            errorMsg = "non-integer classid"

    # non-existing integer classId
    if isError == False:
        try:
            db = Database()
            db.connect()
            classDetails = db.searchClass(classId)
            db.disconnect()

        except Exception as e:
            isError = True
            error = str(e)
            # no class id exists
            if "no class" in error:
                errorMsg = error
            else:
                errorMsg = "A server error occurred. Please contact the system administrator."
                if error == 'database reg.sqlite not found':
                    print('runserver.py: database reg.sqlite not found', file=stderr)
                else:
                    print("runserver.py: " + error, file=stderr)
            

    # get cookies
    prevDept = request.cookies.get('prevDept')
    if prevDept is None:
        prevDept = ""
    prevNum = request.cookies.get('prevNum')
    if prevNum is None:
        prevNum = ""
    prevArea = request.cookies.get('prevArea')
    if prevArea is None:
        prevArea = ""
    prevTitle = request.cookies.get('prevTitle')
    if prevTitle is None:
        prevTitle = ""

    # pass the arguments to Jinja2 and render template,
    html = render_template('templates/regdetails.html',
        classDetails=classDetails,
        isError=isError,
        errorMsg=errorMsg,
        prevDept=prevDept,
        prevNum=prevNum,
        prevArea=prevArea,
        prevTitle=prevTitle,
        classId=classId,
    )
    response = make_response(html)
    return response