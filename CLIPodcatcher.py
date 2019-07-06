from podcatcher import Podcatcher
from Emailer import Emailer
from DownloadLedger import DownloadLedger
from DBA import DBA
from config_reader import Config

podcatcher = Podcatcher()
emailer = Emailer()
downloadLedger = DownloadLedger()
dba = DBA()
config = Config()

if __name__ == '__main__':
    #read from config
    allPodcasts = podcatcher.getListOfPodcasts()
    for podcast in allPodcasts:
        print("Name:" + podcast.name + " that points to: " + podcast.url)
        if config.COPY_CONFIG_TO_DATABASE is True:
            dba.addPodcast(podcast)
    podcatcher.getAllEpisodesForAllPodcasts()
    emailer.sendEmail(downloadLedger.getList())
    downloadLedger.wipeLedger()
