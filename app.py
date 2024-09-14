from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_cors import CORS
import mail_server_props
import base64
import traceback
import mongo_service

app = Flask(__name__)
# for requesting to access the data from another webpage i.e here,javascript cors-cross origin resource sharing
CORS(app)


# home endpoint
@app.route('/')
def index():
    return render_template('home.html')
    # return "Hello World!!"

#compose endpoint
@app.route('/compose')
def compose():
    return render_template('compose.html')


@app.route('/sentmailspage', methods=["GET"])
def sentmailspage():
    return render_template('sent_mails_page.html')



# Sending single mail with Post methods
@app.route('/sendmail', methods=["POST"])
def mail_body():
    # mail_server_props.connect_to_smtp_sever()
    # get data from JSON data of Javascript
    data = request.get_json()
    print("printing email info :", data)
    sender_name = data["sender_name"]
    receiver_name = data["receiver_name"]
    to_email = data["to"]
    print("To: ", to_email)
    sub = data["subject"]
    body = data["body"]
    attachments = data["attachments"]  # attachments 
    # write_to_file(attachments)
    if receiver_name is not None:  
        to_email = f'{receiver_name} <{to_email}>'
        mail_server_props.send_mail_with_details(sender_name, to_email, sub, body, attachments)
    
    else:
        mail_server_props.send_mail_with_details(sender_name, to_email, sub, body, attachments)
    return jsonify({"message" : "Email sent Successfully..!!"})

# sending bulk mails
@app.route('/bulkmails', methods=["POST"])
def bulkmails():
    # mail_server_props.connect_to_smtp_sever()
    # get data from JSON data of Javascript
    data = request.get_json()
    # print("printing email info :", data)
    sender_name = data["sender_name"]
    sub = data["subject"]
    body = data["body"]
    attachments = data["attachments"] 
    to_email = data["to"]
    # write_to_file(attachments)
    for obj in to_email:
        receiver_mail = obj['email']
        receiver_name = obj['receiver_name']
        if receiver_name is not None:  
            receiver_mail = f'{receiver_name} <{receiver_mail}>'
            mail_server_props.send_mail_with_details(sender_name, receiver_mail, sub, body, attachments)
        else:
            mail_server_props.send_mail_with_details(sender_name, receiver_mail, sub, body, attachments)
   
    return jsonify({"message" : "Email sent Successfully..!!"})


def write_to_file(attachments):

    file_name = attachments["file_name"]
    file_content = attachments["file_content"]
    decoded_file = base64.b64decode(file_content)  # decoding the file
    print("write to file : file content : ", decoded_file)  # prints in binary format

    with open(file_name, 'wb') as f:
        f.write(decoded_file)
        f.close()

    pass



# Custom error handler to send back exception messages
@app.errorhandler(Exception)
def handle_exception(e):

    # Log the stack trace (optional, you could log it to a file or system log)
    stack_trace = traceback.format_exc()
    print(stack_trace)

    response = {
        'message': str(e)
    }
    return jsonify(response), 500  # Return a 500 Internal Server Error with the exception message




@app.route('/getsentmails', methods=["GET"])
def getsentmails():
    response = mongo_service.get_all_from_db()
    # print("response : ", response)
    return response



if __name__ == "__main__":
    # app.run(debug = True)
    app.run(host='0.0.0.0', port=5000, debug=True)
