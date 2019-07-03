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
                if key == "downloadLedger":
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
                if key == "dba":
                    self.DBA = value
                if key == "dbaEnabled":
                    self.DBA_ENABLED = value
                if key == "configEnabled":
                    self.CONFIG_ENABLED = value
                if key == "configLocation":
                    self.CONFIG_LOCATION = value
                if key == "copyConfigToDataBase":
                    self.COPY_CONFIG_TO_DATABASE = value
                if key == "removeOldConfig":
                    self.REMOVE_OLD_CONFIG = value
                if key == "copyDatabaseToConfig":
                    self.COPY_DATABASE_TO_CONFIG = value
                if key == "name":
                    self.NAME = value
                if key == "host":
                    self.HOST = value
                if key == "database":
                    self.DATABASE = value
                if key == "password":
                    self.PASSWORD = value
