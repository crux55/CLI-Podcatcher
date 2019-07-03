from config_reader import Config
from PodcastEntity import PodcastEntity

import sqlite3

config = Config()

class DBAsqlite3:

    def __init__(self):
        self.dbname = "podcasts.db"
        self.connection = sqlite3.connect(self.dbname)

    def openConnection(self):
        return sqlite3.connect(self.dbname)

    def closeConnection(self, connection):
        connection.close()

    def addPodcast(self, podcastEntity):
        connection = self.openConnection()
        insert = ("""INSERT INTO Podcasts (name, url, amount, folder_name, offset, from_start, last_updated) 
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');""") \
            .format(podcastEntity.name, podcastEntity.url, podcastEntity.amount, podcastEntity.offset,
                    podcastEntity.fromStart, podcastEntity.lastUpdated)
        cursor = connection.cursor()
        cursor.execute(insert)
        cursor.close()
        connection.close()

    def getPodcastByName(self, name):
        connection = self.openConnection()
        cursor = connection.cursor()
        select = ("""SELECT uid, name, url, amount, folder_name, offset, from_start, last_updated "
                  "FROM Podcasts where name = '{0}';""").format(name)
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
        connection = self.openConnection()
        cursor = connection.cursor()
        select = ("""SELECT uid, name, url, amount, folder_name, offset, from_start, last_updated "
                  "FROM Podcasts;""")
        cursor.execute(select)
        row = cursor.fetchone()
        while row:
            row = cursor.fetchone()
            pod = PodcastEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            allPodcasts.append(pod)
        self.closeConnection(connection)
        return allPodcasts

    def deletePodcastByUid(self, uid):
        connection = self.openConnection()
        cursor = connection.cursor()
        delete = """DELETE FROM Podcasts WHERE uid = '{0}';""".format(uid)
        cursor.execute(delete)
        cursor.close()
        self.closeConnection()

    def deletePodcastByName(self, name):
        connection = self.openConnection()
        cursor = connection.cursor()
        delete = """DELETE FROM Podcasts WHERE name = '{0}';""".format(name)
        cursor.execute(delete)
        cursor.close()
        self.closeConnection()
