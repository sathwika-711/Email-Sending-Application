from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
import mail_server_props
import base64


app = Flask(__name__)
# disable CORS
# cors = CORS(app, resources={r"": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
# for requesting to access the data from another webpage i.e here,javascript cors-cross origin resource sharing
CORS(app)


# home endpoint
@app.route('/')
def index():
    return render_template('home.html')
    # return "Hello World!!"


# Sending mail with Post methods
@app.route('/sendmail', methods=["POST"])
def mail_body():
    # mail_server_props.connect_to_smtp_sever()
    # get data from JSON data of Javascript
    data = request.get_json()
    print("printing email info :", data)
    to_email = data["to"]
    print("To: ", to_email)
    sub = data["subject"]
    body = data["body"]
    attachments = data["attachments"]  # attachments

    # write_to_file(attachments)

    mail_server_props.send_mail_with_details(
        "", to_email, sub, body, attachments)
    # mail_server_props.send_mail(to_email, msg)
    return "Email sent Successfully..!!"


# List to store sent messages
sent_messages = []


@app.route('/sent_emails', methods=['POST'])
def sentEmails():
    global sent_messages
    if request.method == 'POST':
        # Access form data
        # Retrieves the value of the input field with name="to"
        to_email = request.get_json()['to']
        # Retrieves the value of the input field with name="subject"
        subject = request.get_json()['subject']
        # Retrieves the value of the textarea with name="body"
        body = request.get_json()['body']

        # Create a message dictionary
        message = {
            # 'from': from_email,
            'to': to_email,
            'subject': subject,
            'body': body
        }

        print(message)

        # Store the message in the list
        sent_messages.append(message)

        # Redirect to the same page to show messages
        return redirect(url_for('home'))

    # Render the form and display sent messages
    return render_template('home.html', messages=sent_messages)


def write_to_file(attachments):

    file_name = attachments["file_name"]
    file_content = attachments["file_content"]
    decoded_file = base64.b64decode(file_content)  # decoding the file
    print("file content : ", decoded_file)  # prints in binary format

    with open(file_name, 'wb') as f:
        f.write(decoded_file)
        f.close()

    pass


if __name__ == "__main__":
    # app.run(debug = True)
    app.run(host='0.0.0.0', port=5000, debug=True)
