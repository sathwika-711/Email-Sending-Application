from email.mime.text import *
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import os
from dotenv import load_dotenv
import base64
from email.mime.base import MIMEBase
from email import encoders
import mongo_service

# Load environment variables from the .env file
load_dotenv()


# Access the credentials from the environment variables
smtp_server = os.getenv('SMTP_SERVER')
port = int(os.getenv('SMTP_PORT'))
user_name = os.getenv('SMTP_USER_NAME')
password = os.getenv('SMTP_USER_PASSWORD')


# Setting up SMTP
def send_mail(sender_name, subject, body, attachments, receiver_email, email_content):
    # Connect to the server and send the email
    print("connecting to smtp server")

    with SMTP(smtp_server, port) as server:
        try:
            server.starttls()
            print("authenticating to smtp server")
            server.login(user_name, password)
            print("smtp server connected")

            print("sending email")
            server.sendmail(user_name, receiver_email,
                            email_content.as_string())
            
            print(email_content)  # prints the email content in mime format
            # calling insert mail function to send details to insert in mongodb after sending mail (i.e only sent mails are stored in database)
            mongo_service.insert_mail(sender_name, subject, body, attachments, receiver_email)

            print('Email sent successfully!')

        except Exception as e:
            print("Error : ", e)
            raise e


# Sending mail with details
def send_mail_with_details(sender_name, to_email, subject, body, attachments):
    # fetch the attachments
    file_name = attachments["file_name"]
    file_content = attachments["file_content"]
    if sender_name is None:
        sender_name = ""
    sender_name = f'{sender_name} <{user_name}>'
    msg = MIMEMultipart()
    msg['From'] = sender_name
    msg['To'] = to_email
    msg['Subject'] = subject

    if file_name is not None and file_content is not None:
        print("sending attachments")
        decoded_file = base64.b64decode(file_content)  # decoding the file_content
        print("file content : ", decoded_file)  # prints in binary format
        # Create a MIMEBase object for the attachment
        attachMime = MIMEBase('application', 'octet-stream')
        attachMime.set_payload(decoded_file) # Attach the payload to the MIME object
        # Encode the payload using Base64
        encoders.encode_base64(attachMime)
        # Add a header to the attachment
        attachMime.add_header('Content-Disposition',
                              f'attachment; filename="{file_name}"')
        # Attach the file to the email
        msg.attach(attachMime)

    # Create a multipart message
    msg.attach(MIMEText(body, 'html'))

    print("msg : ", msg)
    print("sending email")
    send_mail(sender_name, subject, body, attachments, to_email, msg) #to_email and msg are passed to send a mail, other arguments(also to_emails) are for inserting into database

    return "Email sent successfully.!!"
