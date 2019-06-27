from Emailer import Emailer
from podcatcher import Podcatcher

podcatcher = Podcatcher()

if __name__ == '__main__':
    emailer = Emailer()
    emailer.sendEmail()
    #podcatcher.getAllEpisodesForAllPodcasts()
