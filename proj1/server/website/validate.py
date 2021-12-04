import pandas as pd
import os

RESPONSE_FILE = os.path.dirname(os.path.realpath(
    __file__)) + "/uploads/csv/responses.csv"


def check():
    print(RESPONSE_FILE)
    df = pd.read_csv(RESPONSE_FILE)
    for i in range(len(df)):
        rollno = df.loc[i, "Roll Number"]
        if rollno == "ANSWER":
            return i

    return -1


# print(validate())
