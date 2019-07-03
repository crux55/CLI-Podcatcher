from podcatcher import Podcatcher
from Emailer import Emailer
from DownloadLedger import DownloadLedger
from DBA import DBA
from config_reader import Config
from logger import Logger

podcatcher = Podcatcher()
emailer = Emailer()
downloadLedger = DownloadLedger()
dba = DBA()
config = Config()
logger = Logger()

if __name__ == '__main__':
    #read from config
    logger.info("Starting app")
    logger.info("Getting podcast list")
    allPodcasts = podcatcher.getListOfPodcasts()
    for podcast in allPodcasts:
        logger.log("Name:" + podcast.name + " that points to: " + podcast.link)
        if config.COPY_CONFIG_TO_DATABASE is "true":
            logger.info("Copying config to database")
            dba.addPodcast(podcast)
    logger.log("Download starting")
    podcatcher.getAllEpisodesForAllPodcasts()
    logger.info("Preparing to send email")
    emailer.sendEmail(downloadLedger.getList())
    logger.info("Wiping ledger")
    downloadLedger.wipeLedger()
