"""Creates Canvas Courses

.. moduleauthor:: Jago Brown <jago.brown@lsbm.ac.uk>

.. currentmodule:: Submissions_input_data

:synopsis:
    This file contains data for import by other modules e.g. Submissions_db_import.py.  Principally is stores a list of 
    course_id where these are courses with assessment data required by SIS/Oracle

"""
# TODO consider putting the list of courses (i.e. contents of this file) in a csv file
# Semester from which module assignment data should be pulled
semester = "CheckInputFile"

# Format:  Canvas Course ID , Canvas course code, Assessment IDs or None!
# handle ",," i.e. no value  - by ignoring when substituting  ",None,"

# Explicitly identifying all Canvas assignments

# courses = [[393, "LSBM10021-Sep-16", 1983, 9401, 1924, 1925, 1926, 1927],
#            [934, "LSBM10041-Sep-16", 9115, 9116, 9117, 9118, 9119, 9120],
#            [1243, "LSBM13191-Sep-16", 9259, 12035, 10234, 10223, 11260, 11259]]


# Note When no Assessment ID(s) provided  - all "published" Canvas assignment submissions are pulled:

courses = [[93, "LSBM10021-Sep-16"],
           [131, "LSBM13131-Sep-16"],
           [173, "LSBM13191L-Sep-16"],
           [124, "LSBM13191-Sep-16"],  # NOTE: Jan-17 mods follow:
           [95, "LSBM10011-Jan-17"],
           [125, "LSBM13171-Jan-17"],
           [133, "LSBM13211-Jan-17"],  # NOTE: Apr-17 mods follow:
           [153, "LSBM13001-Apr-17"],
           [247, "LSBM13011-Apr-17"],
           [248, "LSBM13051-Apr-17"],  # NOTE: Jun-17 mods follow:
           [251, "LSBM12051-Jun-17"],
           [252, "LSBM12121-Jun-17"]]