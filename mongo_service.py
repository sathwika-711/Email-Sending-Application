from pymongo import MongoClient
from datetime import datetime

# insert mail
def insert_mail(sender_name, subject, body, attachment, receiver_email):
    # connect to db
    with MongoClient('mongodb://localhost:27017/') as client:
        db = client['EmailPython']
        sent_emails_collection = db['sent_mail']

        print(receiver_email)
        receiver_name = receiver_email.split(' <')[0];
        receiver_email = receiver_email.split('<')[1].replace('>', '');
        print("receiver_name : ", receiver_name)
        print("receiver_email : ", receiver_email)

        # insert mail
        print("inserting mail in db")
        insert_obj = {
            '_timestamp' : datetime.now(),
            'sender_name': sender_name,
            'to_email': receiver_email,
            'receiver_name': receiver_name,
            'subject': subject,
            'body': body,
            'attachment': { 
                'file_type' : attachment['file_type'],
                'file_name' :attachment['file_name'],
                'file_content' : attachment['file_content']
            }
        }
        print("inserting mail in db : ", insert_obj)
        ret_ins = sent_emails_collection.insert_one(insert_obj)  
    
    return ret_ins



def get_all_from_db():
    # connect to db
    with MongoClient('mongodb://127.0.0.1:27017/') as client:
        db = client['EmailPython']
        sent_emails_collection = db['sent_mail']

        # get all mails in reverse chronological order (latest first)
        emails = sent_emails_collection.find({}, {"_id": 0}).sort('_timestamp', -1)
        emails_list = list(emails)
        emails_list
        print("emails : ", emails_list)
        return emails_list   # returns list of all mails to js 