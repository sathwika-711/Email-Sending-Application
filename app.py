from flask import Flask, render_template, request
from flask_cors import CORS
from smtplib import *
import mail_server_props



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


@app.route('/hello')
def hello() :
    return str(1+2)


@app.route('/hello/<val>')
def hello_val(val) :
    print("val : ", val)
    return val


@app.route('/', methods=['POST'])
def post_hello():
    json_body = request.get_json()
    print(json_body)
    # json_body['new'] = 'pair'
    return json_body



# Sending mail with Post methods
@app.route('/mailwithbody', methods=["POST"])
def mail_body():

    # mail_server_props.connect_to_smtp_sever()
    # get data from JSON data of Javascript
    info = request.get_json()
    print("printing email info :", info)
    to_email = info["to"]
    print("To: ",to_email)
    sub = info["subject"]
    body = info["body"]
    msg = f"Subject : {sub}\n\n{body}"
    
    # mail_server_props.send_mail_with_details(to_email, msg)
    mail_server_props.send_mail(to_email, msg)
    return "Email sent Successfully..!!"




if __name__ == "__main__" :
    # app.run(debug = True)
    app.run(host='0.0.0.0', port=5000, debug=True)