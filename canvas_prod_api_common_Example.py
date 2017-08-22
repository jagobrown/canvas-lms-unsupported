"""Common bits of data used in other scripts

.. moduleauthor:: Jago Brown <jago.brown@lsbm.ac.uk>

.. currentmodule:: canvas_prod_api_common_Example

:synopsis:
   Common string variables and constants used in a number of scripts.  There are currently two versions (prod & test) 
   neither of which are saved in the source code repository (git)

"""
# TODO consider changing name of this module to: env_config_settings_prod_Example.py
# Note in scripts that use this CONSTANTS module use '+' str concatenation rater than %s
# ... this caused errors when setting up submissions script after using apicommon.py in pull_Jan-17_course_assignments.py
BASE_URL = "https://canvas.instructure.com/api/v1"  # %s removed /v1%s
access_token = '...40nP'
# Note there may be a db accessible with this str in different environments: Dev, Test, Prod,
# So if script not running in the production environment - the production database will not be updated.
db_connect_str = "dbname='testpython' user='dbuser' host='localhost' password='myOwnPassword'"

# TODO consider adding constants and common functions to another module: common.py or lib.py ?
MSG_SCRIPT_END = "This script has reached the End"

# Linux crontab example:
# */20 7 * * * /usr/bin/python3 /Documents/canvas-lms/grades_csv_for_oracle.py mod 2>>grades_mod_err.log

