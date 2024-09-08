from email.mime.text import *
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import os
from dotenv import load_dotenv
import base64
from email.mime.base import MIMEBase
from email import encoders


# Load environment variables from the .env file
load_dotenv()


# Access the credentials from the environment variables
smtp_server = os.getenv('SMTP_SERVER')
port = int(os.getenv('SMTP_PORT'))
user_name = os.getenv('SMTP_USER_NAME')
password = os.getenv('SMTP_USER_PASSWORD')


# Setting up SMTP
def send_mail(receiver_email, email_content):
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
            print('Email sent successfully!')

        except Exception as e:
            print("Error : ", e)
            raise e


# Sending mail with details
def send_mail_with_details(receiver_email, to_email, subject, body, attachments):
    # fetch the attachments
    file_name = attachments["file_name"]
    file_content = attachments["file_content"]

    msg = MIMEMultipart()
    msg['From'] = receiver_email
    msg['To'] = to_email
    msg['Subject'] = subject

    if file_name is not None and file_content is not None:
        print("sending attachments")

        decoded_file = base64.b64decode(file_content)  # decoding the file
        print("file content : ", decoded_file)  # prints in binary format

        # Create a MIMEBase object for the attachment
        attachMime = MIMEBase('application', 'octet-stream')
        attachMime.set_payload(decoded_file)

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

    send_mail(to_email, msg)

    return "Email sent successfully.!!"
