from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_cors import CORS
import mail_server_props
import base64
import traceback


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
    sender_name = data["sender_name"]
    receiver_name = data["receiver_name"]
    to_email = data["to"]
    print("To: ", to_email)
    sub = data["subject"]
    body = data["body"]
    attachments = data["attachments"]  # attachments 
    # write_to_file(attachments)
    if sender_name is not None and receiver_name is not None:  
        to_email = f'{receiver_name} <{to_email}>'
        mail_server_props.send_mail_with_details(sender_name, to_email, sub, body, attachments)
    
    else:
        mail_server_props.send_mail_with_details(sender_name, to_email, sub, body, attachments)
    return jsonify({"message" : "Email sent Successfully..!!"})


@app.route('/bulkmails', methods=["POST"])
def bulkmails():
    # mail_server_props.connect_to_smtp_sever()
    # get data from JSON data of Javascript
    data = request.get_json()
    print("printing email info :", data)
    sender_name = data["sender_name"]
    sub = data["subject"]
    body = data["body"]
    attachments = data["attachments"] 
    to_email = data["to"]
    for obj in to_email:
        receiver_mail = obj['email']
        receiver_name = obj['receiver_name']
        if sender_name is not None and receiver_name is not None:  
            receiver_mail = f'{receiver_name} <{receiver_mail}>'
            mail_server_props.send_mail_with_details(sender_name, receiver_mail, sub, body, attachments)
        else:
            mail_server_props.send_mail_with_details(sender_name, receiver_mail, sub, body, attachments)
   
    return jsonify({"message" : "Email sent Successfully..!!"})


def write_to_file(attachments):

    file_name = attachments["file_name"]
    file_content = attachments["file_content"]
    decoded_file = base64.b64decode(file_content)  # decoding the file
    print("file content : ", decoded_file)  # prints in binary format

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




if __name__ == "__main__":
    # app.run(debug = True)
    app.run(host='0.0.0.0', port=5000, debug=True)
