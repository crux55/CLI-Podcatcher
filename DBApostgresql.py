from PodcastEntity import PodcastEntity
from config_reader import Config

import psycopg2

config = Config()

class DBApostgres:

    def __init__(self):
        self.name = ""

    def openCOnnection(self):
        return psycopg2.connect(user = config.NAME,
                         password = config.PASSWORD,
                         host = config.HOST,
                         port = "5432",
                         database = config.DATABASE)

    def closeConnection(self, connection):
        connection.close()

    def addPodcast(self, podcastEntity):
        connection = self.openCOnnection()
        cursor = connection.cursor
        insert = ("""INSERT INTO Music.Podcasts (name, url, amount, folder_name, offset, from_start, last_updated) 
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');""")\
            .format(podcastEntity.name, podcastEntity.url, podcastEntity.amount, podcastEntity.offset,
                    podcastEntity.fromStart, podcastEntity.lastUpdated)
        cursor.execute(insert)
        cursor.close()
        self.closeConnection()

    def getPodcastByName(self, name):
        connection = self.openCOnnection()
        cursor = connection.cursor()
        select = ("""SELECT uid, name, url, amount, folder_name, offset, from_start, last_updated "
                  "FROM Music.Podcasts where name = '{0}';""").format(name)
        cursor.execute(select)
        row = cursor.fetchone()
        while row:
            row = cursor.fetchone()
            if row[1] is name:
                self.closeConnection(connection)
                return PodcastEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        self.closeConnection(connection)
        return None

    def getAllPodcasts(self):
        allPodcasts = []
        connection = self.openCOnnection()
        cursor = connection.cursor()
        select = ("""SELECT uid, name, url, amount, folder_name, offset, from_start, last_updated "
                  "FROM Music.Podcasts;""")
        cursor.execute(select)
        row = cursor.fetchone()
        while row:
            row = cursor.fetchone()
            pod = PodcastEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            allPodcasts.append(pod)
        self.closeConnection(connection)
        return allPodcasts

    def deletePodcastByUid(self, uid):
        connection = self.openCOnnection()
        cursor = connection.cursor()
        delete = """DELETE FROM "Music"."Podcasts" WHERE uid = '{0}';""".format(uid)
        cursor.execute(delete)
        cursor.close()
        self.closeConnection()

    def deletePodcastByName(self, name):
        connection = self.openCOnnection()
        cursor = connection.cursor()
        delete = """DELETE FROM "Music"."Podcasts" WHERE name = '{0}';""".format(name)
        cursor.execute(delete)
        cursor.close()
        self.closeConnection()
