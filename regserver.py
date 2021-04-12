#!/usr/bin/env python

#-----------------------------------------------------------------------
# regserver.py
# Author: Bob Dondero
#-----------------------------------------------------------------------
from sys import exit, argv, stderr
from database import Database
from course import Course
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

    # validation
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
        dept=dept,
        num=num,
        area=area,
        title=title,
    )
    return make_response(html)
    
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
            

    # pass the arguments to Jinja2 and render template,
    html = render_template('templates/regdetails.html',
        classDetails=classDetails,
        isError=isError,
        errorMsg=errorMsg,
        classId=classId,
    )
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/courses', methods=['GET'])
def courses():
    dept = request.args.get('dept')
    num = request.args.get('num')
    area = request.args.get('area')
    title = request.args.get('title')
    arguments = [dept, num, area, title]

    courses = None
    html = ''
    try:
        db = Database()
        db.connect()
        courses = db.searchCourses(arguments)
        db.disconnect()

        # format the courses in html
        for course in courses:
            html += "<tr>"
            classId = course.getClassId() 
            html += "<td><a href=regdetails?classid=" + classId + " target='_blank'>" + classId + "</a></td>"
            html += "<td>" + course.getDept() + "</td>"
            html += "<td>" + course.getCrsNum() + "</td>"
            html += "<td>" + course.getArea() + "</td>"
            html += "<td>" + course.getTitle() + "</td>"
            html += "</tr>"
    except Exception as e:
        error = str(e)
        # no class id exists
        errorMsg = "A server error occurred. Please contact the system administrator."
        html += '<div>' + errorMsg + '</div>'
        if error == 'database reg.sqlite not found':
            print('runserver.py: database reg.sqlite not found', file=stderr)
        else:
            print('runserver.py: ' + error, file=stderr)
    
    return  make_response(html)
