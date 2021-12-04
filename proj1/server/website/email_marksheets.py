import pandas as pd
from .email_util import send_mail
import os
from os.path import join, dirname
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

load_dotenv()

SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
print(SMTP_USERNAME, SMTP_PASSWORD)

MSG_BODY = """Dear Student, 

CS384 2021 Quiz 2 marks are attached for reference.
+5 Correct, -1 for wrong.
--
Dr. Mayank"""
SUBJECT = "CS384 2021 - Quiz 2 Regex - with Negative"
SENDER = "code.testing.bot@gmail.com"

BASE_PATH = os.path.dirname(
    os.path.realpath(__file__))
OUTPUT_DIR = BASE_PATH + "/output/rollNumberWise/"
RESPONSE_FILE = BASE_PATH + "/uploads/csv/responses.csv"


def email_marksheets():
    print(OUTPUT_DIR)
    try:
        responses_df = pd.read_csv(RESPONSE_FILE)
        responses_df.set_index(['Roll Number'], inplace=True)
        print("df loaded.")
    except Exception as e:
        raise Exception("Couldn't load data required for sending emails: ") from e
        return

    # Create SMTP object
    print("initiating server...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        print("server running.")
    except Exception as e:
        raise Exception("Couldnt start server: ") from e
        return
    # Login to the server
    try:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("login successful.")
    except:
        # print(SMTP_USERNAME, SMTP_PASSWORD)
        raise Exception("Couldnt Login: ") from e
        return
      
    try:  
        print(os.listdir(OUTPUT_DIR))
        for filename in os.listdir(OUTPUT_DIR):
            if not filename.endswith(".xlsx"):
                continue
            FILEPATH = OUTPUT_DIR + filename
            RECEIVER = responses_df.loc[filename.split('.')[0]]['Email address']

            print("receiver:", RECEIVER)

            send_mail(server, MSG_BODY, SUBJECT, SENDER, RECEIVER, FILEPATH,
                    filename)
                    
        server.close()
        print("Server closed.")
    except Exception as e:
        raise Exception("Couldnt send emails: ") from e
        return
        
    return
