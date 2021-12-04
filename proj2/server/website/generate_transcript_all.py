import os
from .generate_transcript_individual import generate_transcript_for, BASE_PATH
from pathlib import Path


GRADESHEET_DIR = BASE_PATH + "/output/grade_sheets"


def generate():
    arr = os.listdir(GRADESHEET_DIR)
    print("Start")
    for file in arr:
        # print(file)
        # print(Path(file).stem)
        rollno = Path(file).stem
        generate_transcript_for(rollno)
    print("finish")


# generate()
