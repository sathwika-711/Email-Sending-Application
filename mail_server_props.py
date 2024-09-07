from email.mime.text import *
from smtplib import SMTP
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


# Access the credentials from the environment variables
smtp_server = os.getenv('SMTP_SERVER')
port = int(os.getenv('PORT'))
user_name = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')


# Setting up SMTP
def send_mail(receiver_email, email_content) :
    # Connect to the server and send the email

    print("connecting to smtp server")

    with SMTP(smtp_server, port) as server :
        try :
            server.starttls()
            print("authenticating to smtp server")
            server.login(user_name, password)
            print("smtp server connected")

            print("sending email")
            server.sendmail(user_name, receiver_email, email_content)
            print('Email sent successfully!')

        except Exception as e:
            print("Error : ", e)
            raise e  




