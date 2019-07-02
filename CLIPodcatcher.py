from podcatcher import Podcatcher
from Emailer import Emailer
from DownloadLedger import DownloadLedger

podcatcher = Podcatcher()
emailer = Emailer()
downloadLedger = DownloadLedger()

if __name__ == '__main__':
    podcatcher.getAllEpisodesForAllPodcasts()
    emailer.sendEmail(downloadLedger.getList())
    downloadLedger.wipeLedger()
