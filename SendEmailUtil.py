import configparser
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import datetime as datetime

parser = configparser.ConfigParser()
parser.read('notificationConfig.ini')
username = parser['emailCred']['USERNAME']
password = parser['emailCred']['PASSWORD']
sender_email = parser['emailCred']['FROM_EMAIL']
receiver_email = parser['emailCred']['TO_EMAIL']
port = parser['emailCred']['PORT']
smtp_server = parser['emailCred']['SMTP_SERVER']
support_email = parser['emailCred']['SUPPORT_EMAIL']
template_path = parser['emailCred']['TEMPLATE_PATH']
subject = parser['emailCred']['SUBJECT']
sender_name = parser['emailCred']['FROM_NAME']

f = open(template_path, 'r')
file_string = f.read()
f.close()


def send_email(input_ques):
    html = file_string.format(question=input_ques, supportemail=support_email)
    msg = MIMEText(html, "html")
    message = MIMEMultipart("alternative")
    message['From'] = email.utils.formataddr((sender_name, sender_email))
    message['To'] = receiver_email
    message['Subject'] = subject + " Date : " + datetime.datetime.now().strftime("%c")
    message.attach(msg)
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(sender_email, receiver_email.split(","), message.as_string())
        print("Notification Email sent.")
    except Exception as e:
        print("Error occurred while sending email.")
        print(e)
    finally:
        server.quit()
