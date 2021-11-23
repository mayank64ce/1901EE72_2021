import os
import openpyxl
import pandas as pd

ltp_mapping_feedback_type = {1: 'lecture', 2: 'tutorial', 3: 'practical'}

dict1 = {}
dict2 = {}


def stud_info():
    df = pd.read_csv('studentinfo.csv')
    for i in range(len(df)):
        rollno = df.loc[i, "Roll No"]
        email = df.loc[i, "email"]
        aemail = df.loc[i, "aemail"]
        contact = df.loc[i, 'contact']
        name = df.loc[i, 'Name']

        dict1[rollno] = {
            'subjects': {},
            'name': name,
            'email': email,
            'aemail': aemail,
            'contact': contact
        }
    return


def course_master():
    df = pd.read_csv('course_master_dont_open_in_excel.csv')

    for i in range(len(df)):
        subno = df.loc[i, 'subno']
        ltp = df.loc[i, 'ltp'].split('-')
        if subno in dict2:
            continue
        dict2[subno] = []
        for j, s in enumerate(ltp):
            if s != '0':
                dict2[subno].append(j+1)


def courses_registered():
    df = pd.read_csv('course_registered_by_all_students.csv')
    for i in range(len(df)):
        rollno = df.loc[i, "rollno"]
        subno = df.loc[i, "subno"]
        register_sem = df.loc[i, "register_sem"]
        schedule_sem = df.loc[i, "schedule_sem"]
        if subno == 'CE550':
            subno = 'CE543'
        if rollno not in dict1:
            dict1[rollno] = {
                'subjects': {},
                'name': 'NA_IN_STUDENTINFO',
                'email': 'NA_IN_STUDENTINFO',
                'aemail': 'NA_IN_STUDENTINFO',
                'contact': 'NA_IN_STUDENTINFO'
            }

        dict1[rollno]['subjects'][subno] = {
            'ltp': [],
            'register_sem': register_sem,
            'schedule_sem': schedule_sem
        }


def accumulate_feedback():
    df = pd.read_csv('course_feedback_submitted_by_students.csv')

    for i in range(len(df)):
        rollno = df.loc[i, 'stud_roll']
        subno = df.loc[i, 'course_code']
        if subno == 'CE550':
            subno = 'CE543'
        feedback_type = df.loc[i, 'feedback_type']

        if rollno not in dict1:
            continue
        if len(dict2[subno]) == 0:
            continue

        # if subno not in dict1[rollno]['subjects']:
        #     dict1[rollno]['subjects'][subno] = []

        if feedback_type not in dict1[rollno]['subjects'][subno]['ltp']:
            dict1[rollno]['subjects'][subno]['ltp'].append(feedback_type)


def correlate(output_file):

    if not os.path.exists(output_file):
        wb = openpyxl.Workbook()
    else:
        wb = openpyxl.load_workbook(output_file)

    ws = wb['Sheet']
    ws.append(["rollno"	, "register_sem"	, "schedule_sem"	,
               "subno"	, "Name"	, "email"	, "aemail", "contact"])

    for rollno in dict1:
        for subject in dict1[rollno]['subjects']:
            subno = str(subject)
            if subno == 'CE550':
                subno = 'CE543'
            dict1[rollno]['subjects'][subno]['ltp'].sort()
            if dict1[rollno]['subjects'][subno]['ltp'] == dict2[subno]:
                continue

            register_sem = dict1[rollno]['subjects'][subno]['register_sem']
            schedule_sem = dict1[rollno]['subjects'][subno]['schedule_sem']
            name = dict1[rollno]['name']
            email = dict1[rollno]['email']
            aemail = dict1[rollno]['aemail']
            contact = dict1[rollno]['contact']

            ws.append([rollno, register_sem, schedule_sem,
                      subno, name, email, aemail, contact])
            # print(rollno, subno)

    wb.save(output_file)


def feedback_not_submitted():

    output_file_name = "course_feedback_remaining.xlsx"
    stud_info()
    course_master()
    courses_registered()
    accumulate_feedback()
    correlate(output_file_name)


feedback_not_submitted()


# print(dict1['1901CB31'])
# print(dict2['PH110'])
