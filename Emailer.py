import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger import Logger

from config_reader import Config


class Emailer:

    config = Config.instance()
    
    def __init__(self):
        self.senderEmail = self.config.FROM_EMAIL_ADDRESS
        self.receiverEmail = self.config.TO_EMAIL_ADDRESS
        self.emailPassword = self.config.EMAIL_PASSWORD
        self.smtpServer = self.config.EMAIL_SMTP_SERVER
        self.subject = self.config.SUBJECT

    def sendEmail(self, sections):
        htmlHead = """\
        <html>
          <body>
            <p>Hi,<br>
                Here is a list of downloaded music
            </p>
        """
        htlmEnd = """\
        </body>
        </html>
        """

        fullBodyText = htmlHead

        for service in sections.keys():
            fullBodyText += "<br><h1>" + service + "</h1>"
            for show in sections[service].keys():
                fullBodyText += "<br><h2>" + show + "</h2>"
                for i in range(len(sections[service][show])):
                    show_i_ = sections[service][show][i]
                    Logger.debug("Adding text to email: {0}".format(show))
                    fullBodyText += "\n" + show_i_

        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.senderEmail
        message["To"] = self.receiverEmail
        # Turn these into plain/html MIMEText objects
        part2 = MIMEText(fullBodyText, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        Logger.debug("Sending email")
        with smtplib.SMTP_SSL(self.smtpServer, 465, context=context) as server:
            server.login(self.receiverEmail, self.emailPassword)
            server.sendmail(
                self.senderEmail, self.receiverEmail, message.as_string())
