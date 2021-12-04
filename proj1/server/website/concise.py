import json
import os
import pandas as pd
from subprocess import run

BASE_PATH = os.path.dirname(
    os.path.realpath(__file__))

RESPONSE_FILE = BASE_PATH + "/uploads/csv/responses.csv"


def generate_concise():
    print("Generating Concise marksheet.......")
    with open(BASE_PATH + "/stud_info.json") as json_file:
        stud_info = json.load(json_file)

    df = pd.read_csv(RESPONSE_FILE)
    df.rename(columns={'Score': 'Google_Score'}, inplace=True)
    # print(df.columns)
    num_columns = len(df.columns)
    df.insert(loc=num_columns, column='statusAns',
              value=["" for _ in range(len(df))])
    df.insert(loc=6, column='Score_After_Negative',
              value=["" for _ in range(len(df))])
    # print(df.columns)

    for i in range(len(df)):
        rollno = df.loc[i, "Roll Number"]
        df.loc[i, "Score_After_Negative"] = stud_info[rollno]["marks"]
        a = stud_info[rollno]["status"]
        df.loc[i, "statusAns"] = "["+str(a)[1:-1]+"]"

    OUTPUT_PATH = BASE_PATH + "/output/concise/concise_marksheet.csv"

    df.to_csv(OUTPUT_PATH)
    return


def generate_absentees():
    df = pd.read_csv(BASE_PATH + "/output/concise/concise_marksheet.csv")

    with open(BASE_PATH + "/stud_info.json") as json_file:
        stud_info = json.load(json_file)

    columns = df.columns
    print(len(columns))
    num_questions = len(columns) - 10
    print(columns)

    for rollno in stud_info:
        if len(stud_info[rollno]["marks"]) != 0:
            continue

        data = {
            # 'Unnamed: 0': ['-'],
            'Timestamp': ['-'],
            'Email address': ['-'],
            'Google_Score': ['-'],
            'Name': [stud_info[rollno]["name"]],
            'IITP webmail': ['-'],
            'Phone (10 digit only)': ["-"],
            'Score_After_Negative': ['-'],
            'Roll Number': [rollno]
        }

        for j in range(num_questions):
            data['Unnamed: '+str(7+j)] = ["-"]

        data['statusAns'] = ["[]"]

        df2 = pd.DataFrame(data)
        df = pd.concat([df, df2], ignore_index=True, axis=0)

        # print(data)
        # return

    df.to_csv(BASE_PATH + "/output/concise/concise_marksheet.csv")

    print("Concise Marksheet Generated.....")

    return

# generate_concise()


def driver():
    generate_concise()
    generate_absentees()
    
    OUTPUT_CONC_DIR = BASE_PATH + "/output/concise"
    run(f'rm {OUTPUT_CONC_DIR}/placeholder.txt', shell=True)


# driver()
