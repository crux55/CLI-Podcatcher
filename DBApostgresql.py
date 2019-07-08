from PodcastEntity import PodcastEntity
from config_reader import Config
from logger import Logger

import psycopg2

class DBApostgres:

    config = Config.instance()

    def __init__(self):
        self.name = ""

    def openCOnnection(self):
        try:
            Logger.debug("Trying to connect to database")
            da = psycopg2.connect(user = self.config.NAME,
                         password = self.config.PASSWORD,
                         host = self.config.HOST,
                         port = "5432",
                         database = self.config.DATABASE)
            return da
        except Exception as e:
            Logger.error('Failed to connect to database : '+ str(e))

    def closeConnection(self, connection):
        Logger.debug("Connection to database closed")
        connection.close()

    def addPodcast(self, podcastEntity):
        Logger.debug("Trying to add podcast {0} to database".format(podcastEntity))
        connection = self.openCOnnection()
        cursor = connection.cursor()
        sql = ("""INSERT INTO \"Music\".\"Podcasts\" (\"name\", url, amount, folder_name, \"offset\", from_start, last_updated) 
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', NOW());""")\
            .format(podcastEntity.name,
                    podcastEntity.url,
                    podcastEntity.amount,
                    podcastEntity.folderName,
                    podcastEntity.offset,
                    podcastEntity.fromStart,
                    podcastEntity.lastUpdated)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        self.closeConnection(connection)

    def getPodcastByName(self, name):
        Logger.debug("Getting podcast {0} from database".format(name))
        connection = self.openCOnnection()
        cursor = connection.cursor()
        select = ("""SELECT uid, \"name\", url, amount, folder_name, \"offset\", from_start, last_updated "
                  "FROM \"Music\".\"Podcasts\" where \"name\" = '{0}';""").format(name)
        cursor.execute(select)
        row = cursor.fetchone()
        while row:
            if row[1] in name:
                self.closeConnection(connection)
                Logger.debug("Found podcast {0} in database".format(row[1]))
                return PodcastEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            row = cursor.fetchone()
        self.closeConnection(connection)
        return None

    def getAllPodcasts(self):
        Logger.debug("Getting all podcasts from the database")
        allPodcasts = []
        connection = self.openCOnnection()
        cursor = connection.cursor()
        select = ("""SELECT uid, \"name\", url, amount, folder_name, \"offset\", from_start, last_updated "
                  "FROM \"Music\".\"Podcasts\";""")
        cursor.execute(select)
        row = cursor.fetchone()
        while row:
            pod = PodcastEntity(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            allPodcasts.append(pod)
            Logger.debug("Found podcast {0} in database".format(row[1]))
            row = cursor.fetchone()
        self.closeConnection(connection)
        return allPodcasts

    def deletePodcastByUid(self, uid):
        Logger.debug("Deleting podcast with uid {0}".format(uid))
        connection = self.openCOnnection()
        cursor = connection.cursor()
        delete = """DELETE FROM "Music"."Podcasts" WHERE uid = '{0}';""".format(uid)
        cursor.execute(delete)
        cursor.close()
        self.closeConnection()

    def deletePodcastByName(self, name):
        Logger.debug("Deleting podcast with name {0}".format(name))
        connection = self.openCOnnection()
        cursor = connection.cursor()
        delete = """DELETE FROM "Music"."Podcasts" WHERE name = '{0}';""".format(name)
        cursor.execute(delete)
        cursor.close()
        self.closeConnection()
