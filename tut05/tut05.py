import os
import csv
# import openpyxl

# first go through subject_master.csv to get mapping of "Subject_code" to "subject_name"
# then go through names-roll.csv to get mapping of "roll no" to "name"
SUBJECTS_FILE = "subjects_master.csv" 
subjects = []

def get_subjects():
    with(open(SUBJECTS_FILE, 'r') as subject_data):
        for i, row in enumerate(subject_data):
            if i == 0:
                continue
            print(row)
            break
    pass

get_subjects()