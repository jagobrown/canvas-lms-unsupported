#!/usr/bin/env python
"""Gets submission data from Canvas & imports to PostgreSQL DB

.. moduleauthor:: Jago Brown <jago.brown@lsbm.ac.uk>

.. currentmodule:: submissions_postgresql_import

:synopsis:
    Takes a list of Canvas course_id (Submissions_input_data.py), queries Canvas API for each of these & gets all
    submission data for *all* assignments in course.  
    
    Then the script inserts or updates PostgreSQL DB with this data.  This script requires 2 other file(s): Submissions_input_data.py and canvas_prod_api_common.py

"""

# __copyright__ = "Copyright 2017, London School of Business and Management"
# __license__ = ""
# __status__ = "Development"
# __date = "17.8.2017"

import requests
# import json
# import csv # initially this script wrote to CSV

##############
# Start setting different config settings depending on test or production environment:
##############

import canvas_prod_api_common
# import canvas_test_api_common

# access_token = canvas_test_api_common.access_token
# BASE_URL = canvas_test_api_common.BASE_URL
# connect_str = canvas_test_api_common.db_connect_str # was connect_str = canvas_prod_api_common.db_connect_str
# MSG_SCRIPT_END = canvas_test_api_common.MSG_SCRIPT_END

access_token = canvas_prod_api_common.access_token
BASE_URL = canvas_prod_api_common.BASE_URL
connect_str = canvas_prod_api_common.db_connect_str
MSG_SCRIPT_END = canvas_prod_api_common.MSG_SCRIPT_END

##############
# End setting different config settings depending on test or production environment:
##############

import sys
import datetime
import Submissions_input_data  # semesterised INPUT prams for the API query

# load the adapter
import psycopg2

# load the psycopg extras module
# note 17aug17 PyCharm CE on office PC flagged Package requirements 'psycopg2==2.6.2', 'requests==2.12.5' not satisfied! - ignored though
import psycopg2.extras

##############
# Start of functions
##############


def main():
    print('Date today: %s' % datetime.date.today(), ' - to be included in output csv file')

    #: in stderr 1st write today's date
    print('Date today for Stderr: %s' % datetime.date.today(), file=sys.stderr)

    checkNet()

    # TODO catch more exceptions e.g. if: store += r.json() fails !!!
    # TODO org code better - e.g. into more functions ... add write_to_log(message) ...
    # errors where no assignment ID so deleted ,, no values
    # handle ",," i.e. no value  - by ignoring when substituting  ",None," and not creating a uri part etc - done in part


    #  BASE_URL = "https://canvas.lsbm.ac.uk/api/v1"# rm: %s
    #  access_token = '8133~hcAoq...'
    #  REQUEST_HEADERS = {'Authorization':'Bearer %s' % access_token}
    REQUEST_HEADERS = {'Authorization': 'Bearer %s' % access_token}

    fullCourseURIs = CourseURIs()
    # print(fullCourseURIs) # TODO print each course URI on separate line
    # End of generating uri

    # Try to connect

    try:
        # connect_str = "dbname='testpython' user='dbuser' host='localhost' password='myOwnPassword'"
        # declared elsewhere: connect_str = canvas_prod_api_common.db_connect_str # was connect_str = canvas_prod_api_common.db_connect_str
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)

    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e, file=sys.stderr)

    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()

    # If we are accessing the rows via column name instead of position we
    # need to add the arguments to conn.cursor.
    # cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # using uri to pull data from Canvas API then write to Postgres Database

    for course in fullCourseURIs:
        # uri = BASE_URL % '/courses/%s/assignments' % (course_id)
        uri = course
        print("\n\tThe following data is pulled from:\n", uri)

        r = requests.get(uri, headers=REQUEST_HEADERS)
        store = r.json()  # store is a python list of dictionaries
        # print("# var 'store' type: ", type(store))

        # appends more JSON if more pages for API request
        while r.links['current']['url'] != r.links['last']['url']:
            # 10.7.17 modifications made below to find root cause of intermittent TypeError:
            # unsupported operand types(s) for +=: 'dict' and 'dict'... line 163... store+= r.json()
            print(r.links['current']['url'])
            r = requests.get(r.links['next']['url'], headers=REQUEST_HEADERS)
            results = r.json()
            print("r: submissions on this API page: ", results)
            try:
                store += results  # store += r.json()
                # print("store: ", store)
            except Exception as obj:
                print(obj)
                print(obj, file=sys.stderr)

        # print("store: ", store)# for an iteration (course) prints all its submission data

        rowCount = 0
        for item in store:
            rowCount = rowCount + 1
            print("RowCount for this course: ", rowCount)
            # when writing to CSV
            # data = {"id": item["id"], "user_id": item["user_id"], "assignment_id": item["assignment_id"],
            # "score": item["score"], "grade": item["grade"], "grader_id": item["grader_id"],
            # "submitted_at": item["submitted_at"], "graded_at": item["graded_at"], "attempt": item["attempt"]}
            # print (data)
            # csvwriter.writerow(data)

            print("#Data: ", item["id"], item["user_id"], item["assignment_id"],
                  item["score"], item["grade"], item["grader_id"],
                  item["submitted_at"], item["graded_at"], item["attempt"])

            # SQL UPDATE attempted first
            print("SQL UPDATE Begin ", end="")
            # UPDATE public.submissions_dev
            SQL = "UPDATE public.submissions SET id=%s, user_id=%s, assignment_id=%s, score=%s, grade=%s, grader_id=%s, submitted_at=%s, graded_at=%s, attempt=%s WHERE id=%s"

            data = (item["id"], item["user_id"], item["assignment_id"], item["score"], item["grade"], item["grader_id"],
                    item["submitted_at"], item["graded_at"], item["attempt"], item["id"])

            sql_insert_update(conn, cursor, SQL, data)
            print(" - #SQL UPDATE End")

            # SQL INSERT attempted next (probably update & insert should be combined into one sql string)
            # https://stackoverflow.com/questions/1109061/insert-on-duplicate-update-in-postgresql/6527838#6527838
            print("#SQL INSERT Begin ", end="")
            # INSERT INTO public.submissions_dev
            SQL = "INSERT INTO public.submissions(id, user_id, assignment_id, score, grade, grader_id, submitted_at, graded_at, attempt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            data = (item["id"], item["user_id"], item["assignment_id"], item["score"], item["grade"], item["grader_id"],
                    item["submitted_at"], item["graded_at"], item["attempt"])

            sql_insert_update(conn, cursor, SQL, data)
            print("- #SQL INSERT End\n")



    # open a file for writing to CSV

    # Adds semester and date to file name
    # grades_data = open('../data/SubmissionsData-%s_exported-%s.csv' % (Submissions_input_data.semester, datetime.date.today()), 'w', newline='')

    # create the csv writer object
    # note: using DictWriter instead of : csvwriter = csv.writer(grades_data)

    # csv_columns = ['id','user_id','assignment_id','score','grade','grader_id','submitted_at','graded_at','attempt']
    # csvwriter = csv.DictWriter(grades_data, fieldnames=csv_columns)
    # csvwriter.writeheader()
    # close file object
    # grades_data.close()

    # Close communication with the database

    cursor.close()
    conn.close()






# Checks if script can connect to an internet site (if not it will not be able to connect to instructure.com API...
# TODO when working satisfactorily move to this fn to ..._common.py for use in other scripts
def checkNet():
    # import requests
    site = "http://www.google.com"
    try:
        response = requests.get(site)
        print("Response code: " + str(response.status_code) + " from address : " + site, file=sys.stderr)
    except requests.ConnectionError:
        print ("Could not connect to " + site, file=sys.stderr)

# checkNet()




# Generating URIs

def CourseURIs():
    fullCourseURIs = []
    for course in Submissions_input_data.courses: # Submissions_input_data_Apr17
        # print("course list: ",course)
        coursePart = '/courses/%s/students/submissions?student_ids[]=all' % (course[0])
        # print(coursePart)
        courseAssignments = course[2:]
        allCourseAssignments = ""

        for assignment in courseAssignments:
            # print("course item:",assignment)

            if assignment is not None:
                assignmentPart = '&assignment_ids[]=%s' % (assignment)
                # print(assignmentPart)
                allCourseAssignments += assignmentPart
            if assignment is None or not isinstance(assignment, int ):#  type(assignment) not int:
                print("!!!! None or not Integer !!!!")
            # print(allCourseAssignments)
        courseUrl = coursePart + allCourseAssignments
        #print(type(courseUrl), courseUrl)
        # uri = BASE_URL + courseUrl + "&per_page=1000"
        uri = BASE_URL + courseUrl + "&per_page=1000"
        #print(uri)
        fullCourseURIs.append(uri)

    return fullCourseURIs

# fullCourseURIs = CourseURIs()






# Execute SQL
def sql_insert_update(conn, cursor, SQL, data): # (SQL, data):

    try:

        # cursor.execute("""SELECT * from courses""")
        # NOTE 'format' used to include correct SQL in WHERE clause
        cursor.execute(SQL, data) #cursor.execute(sql.format(sql_str))

        # rows = cursor.fetchall()
        # print(rows)
    except Exception as obj:
        print("Error ...", obj)
        # print("Error ...", obj, file=sys.stderr)


    # Make the changes to the database persistent
    conn.commit()



# To guards the code you don't want executed by Sphinx:
if __name__ == "__main__": main()

print(MSG_SCRIPT_END)