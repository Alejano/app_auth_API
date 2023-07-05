    
from __future__ import print_function

  
import base64
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import mimetypes
from mimetypes import guess_type
import os
 
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import time


from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import pandas as pd

import psycopg2
import psycopg2.extras

from dotenv import load_dotenv

import datetime
import pytz

eastern = pytz.timezone("America/Mexico_city")
local_time = datetime.datetime.now()
eastern_time = eastern.localize(local_time)

SCOPES = ['https://mail.google.com/']

from datetime import datetime

# current dateTime
now = datetime.now()

# convert to string
current_time = now.strftime("%Y-%m-%d_%H_%M")
fileName = '{}.csv'.format(current_time)

def create_message(sender, to, subject, message_text):

    message = MIMEMultipart() #when alternative: no attach, but only plain_text
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message['Cc'] = "sergio.martinezc@outlook.com,morakurt@gmail.com"
    ## Part 2   (the message_text)
    # The order count: the first (html) will be use for email, the second will be attached (unless you comment it)
    #message.attach(MIMEText(message_text, 'html'))
    message.attach(MIMEText(message_text, 'plain'))


    my_mimetype, encoding = mimetypes.guess_type(fileName)

    if my_mimetype is None or encoding is not None:
        my_mimetype = 'application/octet-stream' 


    main_type, sub_type = my_mimetype.split('/', 1)# split only at the first '/'

    if main_type == 'text':

        temp = open(fileName, 'r',encoding='ISO-8859-1')  # 'rb' will send this error: 'bytes' object has no attribute 'encode'
        #print(temp.read())
        attachment = MIMEText(temp.read(), _subtype=sub_type)
        temp.close()

    elif main_type == 'image':

        temp = open(fileName, 'rb')
        attachment = MIMEImage(temp.read(), _subtype=sub_type)
        temp.close()

    elif main_type == 'audio':

        temp = open(fileName, 'rb')
        attachment = MIMEAudio(temp.read(), _subtype=sub_type)
        temp.close()            

    elif main_type == 'application' and sub_type == 'pdf':   
        temp = open(fileName, 'rb')
        attachment = MIMEApplication(temp.read(), _subtype=sub_type)
        temp.close()

    else:                              
        attachment = MIMEBase(main_type, sub_type)
        temp = open(fileName, 'rb')
        attachment.set_payload(temp.read())
        temp.close()

    #filename = os.path.basename(fileName)
    attachment.add_header('Content-Disposition', 'attachment', filename=fileName) # name preview in email
    message.attach(attachment) 

    ## Part 4 encode the message (the message should be in bytes)
    message_as_bytes = message.as_bytes() # the message should converted from string to bytes.
    message_as_base64 = base64.urlsafe_b64encode(message_as_bytes) #encode in base64 (printable letters coding)
    raw = message_as_base64.decode()  # need to JSON serializable (no idea what does it means)
    return {'raw': raw} 

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(error)

def genera_csv():
    try:
        # using now() to get current time


        load_dotenv("../.env")
        config = {"user": os.getenv("USER_POSTGRESQL"),
                "password": os.getenv("PASS_POSTGRESQL"),
                "host": os.getenv("HOST_POSTGRESQL"),
                "port": os.getenv("PORT_POSTGRESQL"),
                "database": os.getenv("DB_POSTGRESQL")}

        #config = {"user": "consulta_pr",
        #        "password": 'aB@hB.\1\iY`u3T?',
        #        "host": " 34.132.97.172",
        #        "port": "5432",
        #        "database": "encuestas"}


    except psycopg2.DatabaseError as e:

        # Confirm unsuccessful connection and stop program execution.
        print("Database connection unsuccessful.")
        print(e)
        quit()
  

    try:
        query="""
        SET TIME ZONE 'America/Mexico_city';
        select * from redesc.vw_rep_preregistro_diario;
        """

        with psycopg2.connect(host=config["host"], database=config["database"],
                                   user=config["user"], password=config["password"]) as conn:
            
   
            dat = pd.read_sql_query(query, conn)

        dat.to_csv(fileName, index=False,encoding ='latin1')
        print("Data export successful.")
        time.sleep(10)
        send_mail()
        return True


    except psycopg2.DatabaseError as e:

        # Message stating export unsuccessful.
        print("Data export unsuccessful.")
        quit()

 
    
def send_mail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('jsoncorreo.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    service = build('gmail', 'v1', credentials=creds)
    message = create_message('me', "gaps9233@gmail.com", 'corte del {}, preregistros públicos'.format(now.strftime("%d-%m-%Y")), '')
    print(send_message(service=service, user_id='me', message=message))

if __name__ == '__main__':
    genera_csv()
   