import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config_reader import Config


class Emailer:
    def __init__(self):
        config = Config()
        self.senderEmail = config.FROM_EMAIL_ADDRESS
        self.receiverEmail = config.TO_EMAIL_ADDRESS
        self.emailPassword = config.EMAIL_PASSWORD
        self.smtpServer = config.EMAIL_SMTP_SERVER
        self.subject = config.SUBJECT

    def sendEmail(self):
        html = """\
        <html>
          <body>
            <p>Hi,<br>
               How are you?<br>
               <a href="http://www.realpython.com">Real Python</a> 
               has many great tutorials.
            </p>
          </body>
        </html>
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.senderEmail
        message["To"] = self.receiverEmail
        # Turn these into plain/html MIMEText objects
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtpServer, 465, context=context) as server:
            server.login(self.receiverEmail, self.emailPassword)
            server.sendmail(
                self.senderEmail, self.receiverEmail, message.as_string())






