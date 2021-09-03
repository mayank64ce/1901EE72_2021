"""
@author: mayank64ce

This program categorizes Course information according to Students and Subjects
"""
import os

csv_file = 'regtable_old.csv'
DIR_ROLL_NUMBER = 'output_individual_roll'
DIR_SUBJECT = 'output_by_subject'


def output_by_subject():
    """
        This methods iterates over the given course dataset 
        and puts together all students who took a particular course.
    """
    # print('output_by_subject')
    fo = open(csv_file)
    for i, line in enumerate(fo.readlines()):
        if i == 0:
            continue
        arr = line.split(',')

        file_path = os.path.join(DIR_SUBJECT, arr[3] + '.csv')
        # print(file_path)

        if not os.path.exists(file_path):
            with open(file_path, 'w') as fp:
                fp.write('rollno,register_sem,subno,sub_type\n')

        f = open(file_path, 'a')
        output = arr[0] + ','+arr[1] + ',' + arr[3] + ',' + arr[8]
        f.write(output)
        # if i == 5:
        #     break
    return


def output_individual_roll():
    # print('output_individual_roll')
    """
        This methods iterates over the given course dataset 
        and puts together all courses taken a particular students.
    """
    fo = open(csv_file)
    for i, line in enumerate(fo.readlines()):
        if i == 0:
            continue
        arr = line.split(',')

        file_path = os.path.join(DIR_ROLL_NUMBER, arr[0]+'.csv')

        # print(file_path, dir)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as fp:
                fp.write('rollno,register_sem,subno,sub_type\n')

        f = open(file_path, 'a')
        output = arr[0] + ','+arr[1] + ',' + arr[3] + ',' + arr[8]
        f.write(output)
        # if i == 5:
        #     break
    return


def setup_directories():
    """
        Sets up the output directories
    """
    cwd = os.getcwd()
    if not os.path.isdir(os.path.join(cwd, DIR_ROLL_NUMBER)):
        os.mkdir(os.path.join(cwd, DIR_ROLL_NUMBER))
    if not os.path.isdir(os.path.join(cwd, DIR_SUBJECT)):
        os.mkdir(os.path.join(cwd, DIR_SUBJECT))


# Driver Code
setup_directories()
output_individual_roll()
output_by_subject()
