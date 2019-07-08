import yaml
import os
import requests
from pyPodcastParser.Podcast import Podcast
from config_reader import Config
from logger import Logger
from pathlib import Path
from DownloadLedger import DownloadLedger
from DBA import DBA
from PodcastEntity import PodcastEntity


downloadedFiles = []
PODCAST_INDEX = 0
NAME_FIELD = "name"
AMOUNT_FIELD = "amount"
URL_FIELD = "url"
FOLDER_NAME_FIELD = "folderName"
FROM_START_FIELD = "fromStart"
OFFSET_FIELD = "offset"
PODCAST_FILE_NAME = "podcasts.yml"


class Podcatcher:

    config = Config.instance()
    downloadLedger = DownloadLedger()
    dba = DBA()

    def downloadPodcast(self, fileName, link):
        if Path(fileName).exists():
            Logger.debug("File %s already exists; skipping" % fileName)
            return
        tmpFileName = fileName + ".part"
        with open(tmpFileName, "wb") as f:
            Logger.debug("Downloading to %s" % fileName)
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                os.rename(tmpFileName, fileName)
                downloadedFiles.append(fileName)

    def getListOfPodcasts(self):
        pdcsts = []
        if self.config.CONFIG_ENABLED is True:
            Logger.debug("Looking for podcasts in yaml file: {0}".format(PODCAST_FILE_NAME))
            stream = open(PODCAST_FILE_NAME, "r")
            docs = yaml.safe_load_all(stream)
            for doc in docs:
                for key, value in doc.items():
                    for podcast in value:
                        if OFFSET_FIELD not in podcast:
                            voffset = 1
                        else:
                            #todo check lower limit
                            voffset = podcast[OFFSET_FIELD]
                        if FROM_START_FIELD not in podcast:
                            fromStart = False # todo: test
                        else:
                            fromStart = podcast[FROM_START_FIELD]
                        podcast = PodcastEntity(None, podcast[NAME_FIELD], podcast[URL_FIELD],
                                                podcast[AMOUNT_FIELD], podcast[FOLDER_NAME_FIELD],
                                             voffset, fromStart)
                        Logger.debug("Adding podcast: {0}".format(podcast.name))
                        pdcsts.append(podcast)
        if self.config.DBA_ENABLED is True:
            Logger.debug("Looking for podcasts in the database")
            podcasts = self.dba.getAllPodcasts()
            if len(podcasts) > 0:
                pdcsts += podcasts
        return pdcsts

    def getRSS(self, link):
        response = requests.get(link)
        return Podcast(response.content)

    def getEpisode(self, podcast, episode):
        Logger.warn(episode.enclosure_url)
        link = episode.enclosure_url.encode('ascii', 'ignore').decode('ascii')
        title = episode.title.replace("–", "-").encode('ascii', 'ignore').decode('ascii')
        summary = episode.itunes_summary

        if link is None:
            Logger.warn("An issue had been found whereby this episode has no link to a file. "
                       "It may be a section used for a description. Please white list this"
                       "%s  " % vars(episode))
            return

        Logger.warn("Episode info: [title:%s, link:%s]" % (title, link))

        if self.config.MAKE_FOLDERS and not Path(self.config.BASE_URI + podcast.folderName).exists():
            Logger.debug("Path does not exist, creating")
            os.makedirs(self.config.BASE_URI + podcast.folderName)
        elif not self.config.MAKE_FOLDERS and not Path(self.config.BASE_URI + podcast.folderName).exists():
            Logger.warn("Error: Folder did not exist and can not be created")
            return

        fileExtension = link.rpartition('.')[2]
        fileName = self.config.BASE_URI + podcast.folderName + '/' + str(title) + '.' + fileExtension
        Logger.debug("Found episode with title %s" % str(title))
        self.downloadPodcast(fileName, link)
        self.downloadLedger.addDownload(self.downloadLedger.podcasts, podcast.folderName, title)


    def getAllEpisodesForPodcast(self, podcast):
        offSet = 1
        numberToGet = 0
        Logger.debug("Found podcast with URL %s and amount %d" % (podcast.url, podcast.amount))

        show = self.getRSS(podcast.url)

        if podcast.amount > 0:
            numberToGet = podcast.amount
        elif podcast.amount < 0:
            numberToGet = len(show.items)
        else:
            Logger.debug("Requested no podcasts to be downloaded. This entry is considered a place holder and is ignored")
        Logger.debug("Downloading %d episode(s)" % numberToGet)

        if podcast.fromStart:
            show.items.reverse()

        if podcast.offset:
            offSet = podcast.offset

        for i in range((offSet - 1), numberToGet + (offSet - 1)):
            episode = show.items[i]#can check for null here
            if episode.enclosure_url is not None:
                self.getEpisode(podcast, episode)

    def getAllEpisodesForAllPodcasts(self):
        podcasts = self.getListOfPodcasts()
        for podcastIndex in range(len(podcasts)):
            self.getAllEpisodesForPodcast(podcasts[podcastIndex])
