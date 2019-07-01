import yaml


class Config:
    def __init__(self):
        stream = open("config.yml", "r")
        docs = yaml.safe_load_all(stream)
        for doc in docs:
            for key,value in doc.items():
                if key == "baseURI":
                    self.BASE_URI = value
                if key == "makeFolders":
                    self.MAKE_FOLDERS = value
                if key == "downloadedLedger":
                    self.DOWNLOADED_LEDGER = value
                if key == "allowEmails":
                    self.ALLOW_EMAILS = value
                if key == "fromEmailAddress":
                    self.FROM_EMAIL_ADDRESS = value
                if key == "toEmailAddress":
                    self.TO_EMAIL_ADDRESS = value
                if key == "emailPassword":
                    self.EMAIL_PASSWORD = value
                if key == "smtpServer":
                    self.EMAIL_SMTP_SERVER = value
                if key == "subject":
                    self.SUBJECT = value
