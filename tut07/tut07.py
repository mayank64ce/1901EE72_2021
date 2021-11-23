"""
        @author: mayank64ce
        This program generates a list of all students who have not given 
        the complete feedback for their respective semesters.
    """
import os
import openpyxl
import pandas as pd

ltp_mapping_feedback_type = {1: 'lecture', 2: 'tutorial', 3: 'practical'}

student_info = {}
course_info = {}


def stud_info():
    """
        Pack the needed information from "studentinfo.csv" into a dictionary.
        The information being packed are:
        1. RollNo.
        2. Email
        3. Aemail
        4. Contact
        5. Name
        6. Subjects (taken by the student) (to be filled later on)
    """
    df = pd.read_csv('studentinfo.csv')
    for i in range(len(df)):
        rollno = df.loc[i, "Roll No"]
        email = df.loc[i, "email"]
        aemail = df.loc[i, "aemail"]
        contact = df.loc[i, 'contact']
        name = df.loc[i, 'Name']

        student_info[rollno] = {
            'subjects': {},
            'name': name,
            'email': email,
            'aemail': aemail,
            'contact': contact
        }
    return


def course_master():
    """
        Pack the needed information from "course_master_dont_open_in_excel.csv" 
        into a dictionary.

        The information being packed are:
        1. Subno
        2. its non-zero ltp bits
    """
    df = pd.read_csv('course_master_dont_open_in_excel.csv')

    for i in range(len(df)):
        subno = df.loc[i, 'subno']
        ltp = df.loc[i, 'ltp'].split('-')
        if subno in course_info:
            continue
        course_info[subno] = []
        for j, s in enumerate(ltp):
            if s != '0':
                course_info[subno].append(j+1)


def courses_registered():
    """
        In this method, we fill for each student, all the courses they are taking
        along with its registered and scheduled sem number. 
    """
    df = pd.read_csv('course_registered_by_all_students.csv')
    for i in range(len(df)):
        rollno = df.loc[i, "rollno"]
        subno = df.loc[i, "subno"]
        register_sem = df.loc[i, "register_sem"]
        schedule_sem = df.loc[i, "schedule_sem"]
        if subno == 'CE550':
            subno = 'CE543'
        if rollno not in student_info:
            student_info[rollno] = {
                'subjects': {},
                'name': 'NA_IN_STUDENTINFO',
                'email': 'NA_IN_STUDENTINFO',
                'aemail': 'NA_IN_STUDENTINFO',
                'contact': 'NA_IN_STUDENTINFO'
            }

        student_info[rollno]['subjects'][subno] = {
            'ltp': [],
            'register_sem': register_sem,
            'schedule_sem': schedule_sem
        }


def accumulate_feedback():
    """
        Traverse the feedback CSV file and for each student, put together the feedback 
        of all the subjects they have given the feedback for. (Ignore non credit course)
    """
    df = pd.read_csv('course_feedback_submitted_by_students.csv')

    for i in range(len(df)):
        rollno = df.loc[i, 'stud_roll']
        subno = df.loc[i, 'course_code']
        if subno == 'CE550':
            subno = 'CE543'
        feedback_type = df.loc[i, 'feedback_type']

        if rollno not in student_info:
            continue
        if len(course_info[subno]) == 0:
            continue

        if subno not in student_info[rollno]['subjects']:
            student_info[rollno]['subjects'][subno] = []

        if feedback_type not in student_info[rollno]['subjects'][subno]['ltp']:
            student_info[rollno]['subjects'][subno]['ltp'].append(
                feedback_type)


def correlate(output_file):
    """
    Now for each pair of (student, subno) such that student has taken subno,
    we will check if he/she has given all the required feedback or not.

    Args:
        output_file (str): name of the final output file
    """

    if not os.path.exists(output_file):
        wb = openpyxl.Workbook()
    else:
        wb = openpyxl.load_workbook(output_file)

    ws = wb['Sheet']
    ws.append(["rollno"	, "register_sem"	, "schedule_sem"	,
               "subno"	, "Name"	, "email"	, "aemail", "contact"])

    for rollno in student_info:
        for subject in student_info[rollno]['subjects']:
            subno = str(subject)
            if subno == 'CE550':
                subno = 'CE543'
            student_info[rollno]['subjects'][subno]['ltp'].sort()

            ok = True
            for f in course_info[subno]:
                ok &= f in student_info[rollno]['subjects'][subno]['ltp']
            if ok:
                continue

            try:
                register_sem = student_info[rollno]['subjects'][subno]['register_sem']
                schedule_sem = student_info[rollno]['subjects'][subno]['schedule_sem']
                name = student_info[rollno]['name']
                email = student_info[rollno]['email']
                aemail = student_info[rollno]['aemail']
                contact = student_info[rollno]['contact']
            except:
                print(rollno, subno, "************************")

            ws.append([rollno, register_sem, schedule_sem,
                      subno, name, email, aemail, contact])
            # print(rollno, subno)

    wb.save(output_file)

# Driver method


def feedback_not_submitted():

    output_file_name = "course_feedback_remaining.xlsx"
    stud_info()
    course_master()
    courses_registered()
    accumulate_feedback()
    correlate(output_file_name)


feedback_not_submitted()
