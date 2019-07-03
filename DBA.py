from config_reader import Config
from DBApostgresql import DBApostgres
from DBAsqlite3 import DBAsqlite3


class DBA:

    def __init__(self):
        config = Config()
        if config is "postgres":
            self.dba = DBApostgres()
        if config is "sqlite3":
            self.dba = DBAsqlite3()

    def addPodcast(self, podcast):
        if self.getPodcastByName(podcast.name) is None:
            self.dba.addPodcast(podcast)

    def getPodcastByName(self, name):
        return self.dba.getPodcastByName(name)

    def getAllPodcasts(self):
        return self.dba.getAllPodcasts()

    def deletePodcastByUid(self, uid):
        self.dba.deletePodcastByUid(uid)

    def deletePodcastByName(self, name):
        self.dba.deletePodcastByName(name)

