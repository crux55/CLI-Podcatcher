from config_reader import Config


class DownloadLedger:

    def __init__(self):
        config = Config()
        self.podcasts = "Podcasts"
        self.podcastLedger = config.DOWNLOADED_LEDGER

    def addDownload(self, service, item):
        if service == self.podcasts:
            f= open(self.podcastLedger,"w+")
            f.write(item['name'] + item['url'])
            f.close()
