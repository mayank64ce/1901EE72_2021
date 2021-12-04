from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib


def send_mail(server, MESSAGE_BODY, EMAIL_SUBJECT, EMAIL_FROM, EMAIL_TO, PATH_TO_CSV_FILE, FILE_NAME):
    # Create a multipart message
    print("Initiating msg...")
    try:
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

    except Exception as e:
        raise Exception("Couldn't create message: ") from e
        return
        # try:
            # Convert the message to a string and send it
    try:
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        print("msg sent successfully!")
    except Exception as e:
        raise Exception("Couldnt send message: ") from e
        return

    return
