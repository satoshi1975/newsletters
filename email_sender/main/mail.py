import time
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template import Context, Template
from .models import SentMessage,Subscriber
from django.contrib.auth.models import User

HTML_CONTENT = """
<html>
<head></head>
<body>
    <p>$body</p>
    <img src="http://127.0.0.1:8000/img/$track_num" alt="">
</body>
</html>"""


def generate_unique_track_number():
    """create unique number for tracking by 1px photo"""
    timestamp = int(time.time())  
    random_part = random.randint(1000, 9999)  
    return "{timestamp}{random_part}".format(
        timestamp=timestamp,
        random_part=random_part
    )
 
def message_text(recipient,subject,body,sender_email,track_number):
    """message body formater"""
    context_text = Context({
    "first_name": recipient['first_name'],
    "last_name": recipient['last_name'],
    "email":recipient['email'],
    "date_of_birth":recipient['date_of_birth']
    })
    
    body = body.render(context_text).encode('utf-8')
    temp_body=string.Template(HTML_CONTENT)
    res_body = temp_body.substitute(body = body, track_num  = track_number)
    
    message = MIMEMultipart()
    message.attach(MIMEText(res_body,'html'))
    message['From'] = sender_email
    message['To'] = recipient['email']
    message['Subject'] = subject
    
    return {'message':message,'body':body}

def send_email(email_data):
    """connect to email and send emails func"""
    sender_email = email_data['sender_email']
    sender_password = email_data['sender_password']
    subject =email_data['subject']
    body = Template(email_data['message_template'])
    track_number = generate_unique_track_number()
    
    try: #connect to sender email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        for recipient in email_data['list_of_recipients']: #cycle for all recipients
            message = message_text(recipient,subject,body,sender_email, track_number) #creating a message body
            try:
                
                server.sendmail(sender_email, recipient['email'],
                                message['message'].as_string()) #sending a message to a user
                SentMessage.objects.create( #create new sent message
                    user = User.objects.get(id = email_data['sender_id']),
                    recipient = Subscriber.objects.get(id = recipient['id']),
                    status = 'sent',
                    message = message['body'],
                    track_num = track_number,
                )
            except Exception as e:
                print('Email sending failed:', str(e))
        server.quit()
    except Exception as e:
        print('Excaptions:', str(e))
