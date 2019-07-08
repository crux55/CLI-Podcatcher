from config_reader import Config
from DBApostgresql import DBApostgres
from logger import Logger

class DBA:

    config = Config.instance()

    def __init__(self):
        Logger.debug("Setting DBA to instance of {0}".format('postgres'))
        self.dba = DBApostgres()

    def addPodcast(self, podcast):
        if self.getPodcastByName(podcast.name) is None:
            Logger.debug("Adding podcast with Name: {0}".format(podcast.name))
            self.dba.addPodcast(podcast)
        else:
            Logger.warn("Podcast with name {0} already exists".format(podcast.name))

    def getPodcastByName(self, name):
        Logger.debug("Getting podcast with name {0}".format(name))
        return self.dba.getPodcastByName(name)

    def getAllPodcasts(self):
        Logger.debug("Getting all podcasts from database")
        return self.dba.getAllPodcasts()

    def deletePodcastByUid(self, uid):
        Logger.debug("Getting podcast with uid {0}".format(uid))
        self.dba.deletePodcastByUid(uid)

    def deletePodcastByName(self, name):
        Logger.debug("Deleting podcast with name {0}".format(name))
        self.dba.deletePodcastByName(name)

