from config_reader import Config


class DownloadLedger:

    def __init__(self):
        config = Config()
        self.podcasts = "Podcasts"
        self.podcastLedger = config.DOWNLOADED_LEDGER
        self.DELIMITER = "#!#"

    def addDownload(self, service, show, title):
        if service == self.podcasts:
            f = open(self.podcastLedger, "a")
            f.write(service + self.DELIMITER + show + self.DELIMITER + title + "\n")
            f.close()

    def getList(self):
        serviceMap  = dict()
        f = open(self.podcastLedger, "r")
        if f.mode == 'r':
            lines = f.readlines()
            for line in lines:
                parts = line.split(self.DELIMITER)
                service = parts[0]
                show = parts[1]
                title = parts[2]
                if service not in serviceMap.keys():
                    serviceMap[service] = dict()
                if show not in serviceMap[service].keys():
                    serviceMap[service][show] = ()
                serviceMap[service][show] = serviceMap[service][show] + (title,)
        return serviceMap

    def wipeLedger(self):
        f = open(self.podcastLedger, 'r+')
        f.truncate(0) # need '0' when using r+
