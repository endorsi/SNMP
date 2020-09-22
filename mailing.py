import smtplib,ssl
from email.mime.text import MIMEText


def sendemail(sender_email, receiver_email, password2, msg2):
    port = 465
    smtp_server = "smtp.gmail.com"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password2)
        server.sendmail(sender_email, receiver_email, msg2)

msg = MIMEText(' mail')
msg['Subject'] = 'Test  !'

sendemail('user','target','pass',msg.as_string())
