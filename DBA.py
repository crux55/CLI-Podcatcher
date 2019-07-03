from config_reader import Config
from DBApostgresql import DBApostgres
from DBAsqlite3 import DBAsqlite3
from logger import Logger

logger = Logger()

class DBA:

    def __init__(self):
        config = Config()
        dba = config.DBA
        logger.info("Setting DBA to instance of {0}".format(dba))
        if dba is "postgres":
            self.dba = DBApostgres()
        if dba is "sqlite3":
            self.dba = DBAsqlite3()

    def addPodcast(self, podcast):
        if self.getPodcastByName(podcast.name) is None:
            logger.log("Adding podcast with Name: {0}".format(podcast.name))
            self.dba.addPodcast(podcast)
        else:
            logger.warn("Podcast with name {0} already exists".format(podcast.name))

    def getPodcastByName(self, name):
        logger.info("Getting podcast with name {0}".format(name))
        return self.dba.getPodcastByName(name)

    def getAllPodcasts(self):
        logger.info("Getting all podcasts")
        return self.dba.getAllPodcasts()

    def deletePodcastByUid(self, uid):
        logger.info("Getting podcast with uid {0}".format(uid))
        self.dba.deletePodcastByUid(uid)

    def deletePodcastByName(self, name):
        logger.info("Deleting podcast with name {0}".format(name))
        self.dba.deletePodcastByName(name)

