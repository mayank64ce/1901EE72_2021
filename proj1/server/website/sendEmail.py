#not using this file

import pandas as pd
import os
from email_util import send_email

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib


def send_mail():
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText(MESSAGE_BODY, 'plain')
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    with open(PATH_TO_CSV_FILE, 'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=FILE_NAME))

    # Create SMTP object
    smtp_obj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    # Login to the server
    smtp_obj.login(SMTP_USERNAME, SMTP_PASSWORD)

    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()


OUTPUT_DIR = os.path.dirname(os.path.realpath(
    __file__)) + "/output/rollNumberWise/"
SUBJECT = "pfa"
SENDER =


def send_to_one(filepath, sender, receiver, subject):
    return True


def send_email():
    print(OUTPUT_DIR)
    for(filename in os.listdir(OUTPUT_DIR)):
        if(not filename.endswith(".csv")):
            continue
        FILEPATH = OUTPUT_DIR + filename
        RECEIVER =

        send_to_one(FILEPATH, SENDER, RECEIVER, SUBJECT)

    return False


# print(send_email())
