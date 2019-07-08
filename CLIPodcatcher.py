from config_reader import Config
from podcatcher import Podcatcher
from Emailer import Emailer
from DownloadLedger import DownloadLedger
from DBA import DBA
from logger import Logger


podcatcher = Podcatcher()
emailer = Emailer()
downloadLedger = DownloadLedger()
dba = DBA()

class CLIPodcatcher:

    config = Config.instance()

    def __init__(self):
        Logger.info("Application starting")
        allPodcasts = podcatcher.getListOfPodcasts()
        for podcast in allPodcasts:
            Logger.debug("Name:" + podcast.name + " that points to: " + podcast.url)
            if self.config.COPY_CONFIG_TO_DATABASE is True:
                Logger.info("Copying config to database")
                dba.addPodcast(podcast)
        Logger.info("Download starting")
        podcatcher.getAllEpisodesForAllPodcasts()
        Logger.info("Preparing to send email")
        emailer.sendEmail(downloadLedger.getList())
        Logger.info("Wiping ledger")
        downloadLedger.wipeLedger()


CLIPodcatcher()