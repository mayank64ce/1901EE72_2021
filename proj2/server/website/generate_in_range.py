import os
import pandas as pd
from .generate_transcript_individual import generate_transcript_for, get_details, BASE_PATH
from subprocess import run

TRANSCRIPT_DIR = BASE_PATH + "/output/transcriptsIITP/"
GRADES = BASE_PATH + "/uploads/csv/grades.csv"


def generate_in_range(start, end):

    print("Hiyaaa!!")

    df = pd.read_csv(GRADES)
    not_found = []
    rollnos = df['Roll'].unique()

    print(rollnos)

    try:
        if start[:6] != end[:6]:
            # Throw Error
            print("ERRROOOOORRRR!!!!")
            raise Exception("Invalid Range")
    except:
        raise Exception("Invalid Range")
    print("Helo1")
    base = start[:6]

    num_start = int(start[6:])
    num_end = int(end[6:])

    if num_start > num_end:
        num_start, num_end = num_end, num_start

    print("Helo2")

    for x in range(num_start, num_end+1):
        num = str(x)
        if len(num) == 1:
            num = "0"+num
        rollno = base + num
        if rollno not in rollnos:
            print("whaaat", rollno, base)
            not_found.append(rollno)
            continue
        print(rollno)
        try:
            generate_transcript_for(rollno)
        except:
            raise Exception("There is a problem in individual Generator")

    print("Done finally")

    return not_found
