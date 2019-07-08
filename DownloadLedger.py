from config_reader import Config
from logger import Logger


class DownloadLedger:

    config = Config.instance()

    def __init__(self):
        self.podcasts = "Podcasts"
        self.podcastLedger = self.config.DOWNLOADED_LEDGER
        self.DELIMITER = "#!#"

    def addDownload(self, service, show, title):
        if service == self.podcasts:
            Logger.debug("Adding podcast {0} :: {1} :: to download list")
            f = open(self.podcastLedger, "a")
            f.write(service + self.DELIMITER + show + self.DELIMITER + title + "\n")
            f.close()

    def getList(self):
        Logger.debug("Getting shows from download ledger")
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
        Logger.debug("Wiping download ledger")
        f = open(self.podcastLedger, 'r+')
        f.truncate(0) # need '0' when using r+
