import sys
import yaml
import os

from pyPodcastParser.Podcast import Podcast
import requests

from podcastEntry import PodcastEntry
from logger import Logger
from pathlib import Path
from config_reader import Config

from youtubedl import YoutubeDL

from pprint import pprint

logger = Logger()
config = Config()

downloadedFiles = []


def getPodcast(fileName, url):
    if Path(fileName).exists():
        logger.log("File %s already exists; skipping" % fileName)
        return
    tmpFileName = fileName + ".part"
    with open(tmpFileName, "wb") as f:
        logger.log("Downloading to %s" % fileName)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            lastDone = -1
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(100 * dl / total_length)
                if done > lastDone:
                    logger.log("%s done" % done)
                    lastDone = done
                sys.stdout.write("\r[%s done]" % (done) )
                sys.stdout.flush()
            os.rename(tmpFileName, fileName)
            downloadedFiles.append(fileName)


def getListOfPodcasts():
    logger.log("Getting pod cast list")
    pdcsts = []
    stream = open("podcasts.yml", "r")
    docs = yaml.safe_load_all(stream)
    for doc in docs:
        for key, value in doc.items():
            if "offset" not in value:
                voffset = 1
            else:
                #todo check lower limit
                voffset = value["offset"]
            if "fromStart" not in value:
                fromStart = False
            else:
                fromStart = value["fromStart"]
            pdcsts.append(PodcastEntry(value["amount"], value["url"], value["folderName"], voffset, fromStart))
    return pdcsts


if __name__ == '__main__':
    podcasts = getListOfPodcasts()
    for podcastIndex in range(len(podcasts)):
        offSet = 1
        numberToGet = 0

        podcast = podcasts[podcastIndex]
        logger.log("Found podcast with URL %s and amount %d" % (podcast.link, podcast.amount))

        response = requests.get(podcast.link)
        show = Podcast(response.content)

        if podcast.amount > 0:
            numberToGet = podcast.amount
        elif podcast.amount < 0:
            numberToGet = len(show.items)
        else:
            logger.log("Requested no podcasts to be downloaded. This entry is considered a place holder and is ignored")
        logger.log("Downloading %d episode(s)" % numberToGet)

        if podcast.fromStart:
            show.items.reverse()


        if podcast.offset:
            offSet = podcast.offset

        for i in range((offSet - 1), numberToGet + (offSet - 1)):
            episode = show.items[i]
            link = episode.enclosure_url
            title = episode.title.replace("–", "-")# replace utf-8 symbol (ndash) to ascii (-)
            summary = episode.itunes_summary

            if link is None:
                logger.log("An issue had been found whereby this episode has no link to a file. "
                           "It may be a section used for a description. Please white list this"
                           "%s" % vars(episode))
                continue

            logger.log("Episode info: [title:%s, link:%s]" % (title.encode('utf8'), link.encode('utf8')))

            if config.MAKE_FOLDERS and not Path(config.BASE_URI + podcast.folderName).exists():
                logger.log("Path does not exist, creating")
                os.makedirs(config.BASE_URI + podcast.folderName)
            elif not config.MAKE_FOLDERS and not Path(config.BASE_URI + podcast.folderName).exists():
                logger.log("Error: Folder did not exist and can not be created")
                continue

            fileExtension = link.rpartition('.')[2]
            fileName = config.BASE_URI + podcast.folderName + '/' + str(title.encode('utf8')) + '.' + fileExtension
            logger.log("Found episode with title %s" % str(title.encode('utf8')))
            logger.log(fileName)
            getPodcast(fileName, link)
