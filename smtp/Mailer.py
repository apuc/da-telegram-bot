from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl


class Mailer:

    def __init__(self):
        from smtp import config
        self.config = config
        self.msg = MIMEMultipart()
        self.message = None
        self.server = None

    def prepare(self):
        self.set_data()

    def connect_to_server(self):
        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(self.config['SMTP_HOST'], self.config['SMTP_PORT'], context=context)

        # self.server.starttls()

        # Login Credentials for sending the mail
        self.server.login(self.config['SMTP_USER'], self.config['SMTP_PASS'])

    def set_data(self):
        self.msg['From'] = self.config['SMTP_USER']
        self.msg['To'] = self.config['ADMIN_EMAIL']
        self.msg['Subject'] = "Предложили новость"

    def set_message(self, message):
        self.msg.attach(MIMEText(message, 'plain'))

    def send(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.config['SMTP_HOST'], self.config['SMTP_PORT'], context=context) as server:
            server.login(self.config['SMTP_USER'], self.config['SMTP_PASS'])
            server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            print('mail successfully sent')
            server.quit()
        # self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
