import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = 'da@rabota.today'
receivers = ['apuc06@mail.ru']

port = 465
user = 'da@rabota.today'
password = '123edsaqw'

# msg = MIMEText('This is test mail')
msg = MIMEMultipart()

msg['Subject'] = 'Test mail'
msg['From'] = 'da@rabota.today'
msg['To'] = 'apuc06@mail.ru'

msg.attach(MIMEText('Привет как дела?', 'plain'))

context = ssl.create_default_context()

with smtplib.SMTP_SSL("mail.adm.tools", port, context=context) as server:

    server.login(user, password)
    server.sendmail(sender, receivers, msg.as_string())
    print('mail successfully sent')