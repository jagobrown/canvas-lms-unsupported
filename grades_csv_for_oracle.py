#!/usr/bin/python3
"""CSV output of Canvas Grades data 

.. moduleauthor:: Jago Brown <jago.brown@lsbm.ac.uk>

.. currentmodule:: grades_csv_for_oracle

:synopsis:
    Takes a command line arg [ini|mod|final], Queries PostgreSQL Database (which is populated by 
    submissions_db_import.py... and then outputs a CSV file for later consumption 

"""

# __copyright__ = "Copyright 2017, London School of Business and Management"
# __license__ = ""
# __status__ = "Development"
# __date = "7.6.2017"


# Note: SQL WHERE clause now requires each row has an integration_id AND sis_user_id AND this starts 'LON'
# WHERE a.integration_id IS NOT NULL
# AND u.sis_user_id IS NOT NULL
# AND left(u.sis_user_id, 3) = 'LON'


# if script failing check python processes running
# pgrep -af python

# load the adapter
import psycopg2

# load the psycopg extras module
import psycopg2.extras

import csv
import canvas_prod_api_common
# import time # not used in submissions_MonYY.py
import datetime
# from pprint import pprint # used for logging
from sys import argv

# Set default grade type
grade_type = "final"# "A1orA2"
# 24.7.17 modification to include Resit grades in Final CSV
# sql_grd_type_str_default = "AND (right(a.integration_id, 3) =  '-A1' OR right(a.integration_id, 3) =  '-A2')"
sql_grd_type_str_default = "AND s.score IS NOT NULL AND ((right(a.integration_id, 4) = '-A1r' \
OR right(a.integration_id, 4) = '-A2r') \
OR (right(a.integration_id, 3) = '-A1' OR right(a.integration_id, 3) =  '-A2'))"
sql_grd_type_str = sql_grd_type_str_default

# Enable cmd line argument [1] to set grade type returned - by query by modifying query
# e.g.
# /home/user/python grades_csv_for_oracle.py mod
# /home/user/python grades_csv_for_oracle.py ini
# /home/user/python grades_csv_for_oracle.py final # A1orA2

# TODO use try/except to hand errors like when no args are supplied - IndexError: list index out of range

if argv[1] == "ini":
    grade_type = "ini"
    sql_grd_type_str = "AND right(a.integration_id, 4) =  '-ini'"
    csv_columns = ['grade_identifier', 'Initial Grade (Letter)', 'Initial Grade (Number)']

# Moderator grade
elif argv[1] == "mod":
    grade_type = "mod"
    sql_grd_type_str = "AND right(a.integration_id, 4) =  '-mod'"
    csv_columns = ['grade_identifier', 'Moderator Grade (Letter)', 'Moderator Grade (Number)', 'Moderated By',
                   'Moderated Date']

elif argv[1] == "final": # "A1orA2":
    sql_grd_type_str = sql_grd_type_str_default
    # Final grade column names
    csv_columns = ['grade_identifier', 'Agreed Grade (Letter)', 'Agreed Grade (Number)', 'Marked By', 'Marked Date',
                   'Submission Date']

# print to screen
print("# Date: ", datetime.date.today())
print("argv[0]: ", argv[0])
print("argv[1]: ",argv[1])

# filename
# grades_dump_filename = '../data/grades_%s_%s.csv' % (grade_type, datetime.date.today()) # used for local testing
grades_dump_filename = '/srv/VLE/Canvas/grades_%s_%s.csv' % (grade_type, datetime.date.today())


# SQL query to Postgres
sql = """SELECT
	CASE WHEN a.integration_id LIKE '%-mod' THEN u.sis_user_id || '-' || replace(a.integration_id ,'-mod','')
    	 WHEN a.integration_id LIKE '%-ini' THEN u.sis_user_id || '-' || replace(a.integration_id ,'-ini','')
         WHEN a.integration_id != '' THEN u.sis_user_id || '-' || a.integration_id
         ELSE ''
    END AS "oracle_grade_identifier",
a.integration_id AS "Agreed_Ini_Mod",
s.score AS "Number",
s.grade AS "Letter",
uGrader.name AS "Grader",
s.graded_at AS "Graded_at",
-- a.name AS "Canvas_Ass_Name",
-- , c.name AS "CourseName", c.sis_course_id, s.grader_id,
-- u.sis_user_id, -- u.integration_id AS "UN_num",
-- a.course_id, a.grading_standard_id, a.points_possible, a.grading_type, s.id AS "submissionID", s.assignment_id AS "AssignID", 
s.submitted_at AS "Submitted_at"
--, s.attempt
FROM public.submissions s
LEFT JOIN public.users u ON s.user_id = u.id
LEFT JOIN public.users uGrader ON s.grader_id = uGrader.id
LEFT JOIN public.assignments a ON a.id = s.assignment_id
JOIN public.courses c ON c.id = a.course_id
WHERE a.integration_id IS NOT NULL
AND u.sis_user_id IS NOT NULL
AND left(u.sis_user_id, 3) = 'LON'
-- AND right(a.integration_id, 4) =  '-mod'
-- AND right(a.integration_id, 4) =  '-ini'
-- AND (right(a.integration_id, 3) =  '-A1' OR right(a.integration_id, 3) =  '-A2')
-- AND enrollment_term_id = 7 -- !!! ONLY FOR TESTING to limit returned rows
{0}
ORDER BY c.sis_course_id, u.name, a.integration_id"""

def main():
    # Try to connect
    try:
        # connect_str = "dbname='testpython' user='dbuser' host='localhost' password='myOwnPassword'"
        connect_str = canvas_prod_api_common.db_connect_str
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)

    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)


    # create a psycopg2 cursor that can execute queries
    # cursor = conn.cursor()
    # If we are accessing the rows via column name instead of position we
    # need to add the arguments to conn.cursor.
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:

        # cursor.execute("""SELECT * from courses""")
        # NOTE 'format' used to include correct SQL in WHERE clause
        cursor.execute(sql.format(sql_grd_type_str))
        # cursor.execute(sql)
        # rows = cursor.fetchall()
        # print(rows)
    except:
        print("I can't SELECT from ...")

    #
    # Note that below we are accessing the row via the column name.

    rows = cursor.fetchall()
    # Note: keep this for loop for when you want to check & print to screen data returned by SQL query
    for row in rows:
        print(row, type(row))
        # numeric ref example: print("   ", row[2])
        # print("List items called individually: ", row['oracle_grade_identifier'],row['Agreed_Ini_Mod'],row['Number'],row['Letter'] )

    write_csv(rows)



def write_csv(rows):

    # grades_data = open('../data/grades_%s_%s.csv' % (grade_type, datetime.date.today()),'w', newline='')
    grades_data = open(grades_dump_filename, 'w', newline='')


    # create the csv writer object
    # note: using DictWriter instead of : csvwriter = csv.writer(grades_data)
    print("!"* 5," Grade Type written to CSV: ", grade_type )
    # csv_columns = ['oracle_grade_identifier', 'Agreed_Ini_Mod', 'Number', 'Letter']

    csvwriter = csv.DictWriter(grades_data, fieldnames=csv_columns)
    csvwriter.writeheader()

    rowCount = 0
    for row in rows:
        rowCount = rowCount + 1
        # print(rowCount)

        #data = {"oracle_grade_identifier": row["oracle_grade_identifier"], "Agreed_Ini_Mod": row["Agreed_Ini_Mod"], "Number": row["Number"],
        #       "Letter": row["Letter"]}
        if grade_type == "ini":
            # For 'Initial grade'
            data = {"grade_identifier": row["oracle_grade_identifier"],  # "Agreed_Ini_Mod": row["Agreed_Ini_Mod"],
                    "Initial Grade (Letter)": row["Letter"],
                    "Initial Grade (Number)": row["Number"]}

        elif  grade_type == "mod":
            # For 'Moderators grade'
            data = {"grade_identifier": row["oracle_grade_identifier"],  # "Agreed_Ini_Mod": row["Agreed_Ini_Mod"],
                    "Moderator Grade (Letter)": row["Letter"],
                    "Moderator Grade (Number)": row["Number"],
                    "Moderated By": row["Grader"],
                    "Moderated Date": row["Graded_at"]}

        elif grade_type == "final": # 'A1orA2':
            # For 'Final grade'
            data = {"grade_identifier": row["oracle_grade_identifier"], #"Agreed_Ini_Mod": row["Agreed_Ini_Mod"],
                   "Agreed Grade (Letter)": row["Letter"],
                    "Agreed Grade (Number)": row["Number"],
                    "Marked By": row["Grader"],
                    "Marked Date": row["Graded_at"],
                    "Submission Date": row["Submitted_at"]}

        csvwriter.writerow(data)
    print("rows written to CSV: ", rowCount)

    # close file object
    grades_data.close()


# TODO add logging
# def write_to_log(message):
#     with open(log_file, 'a') as log:
#         log.write(message + "\n")
#         pprint(message)

if __name__ == "__main__": main()

print(canvas_prod_api_common.MSG_SCRIPT_END)
