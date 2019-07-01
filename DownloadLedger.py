from config_reader import Config


class DownloadLedger:

    def __init__(self):
        config = Config()
        self.podcasts = "Podcasts"
        self.podcastLedger = config.DOWNLOADED_LEDGER
        self.DELIMITER = "#!#"

    def addDownload(self, service, title, link):
        if service == self.podcasts:
            f= open(self.podcastLedger,"w+")
            f.write(title + self.DELIMITER + link)
            f.close()
