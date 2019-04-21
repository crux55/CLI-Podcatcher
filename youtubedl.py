from __future__ import unicode_literals
import youtube_dl
import yaml
import sqlite3
from youtubeEntity import YoutubeEntity

class YoutubeDL:


    def __init__(self):
        self.y = "y"

    def get(self):
        # for score, recording_id, title, artist in acoustid.match("25H18MUzMh", "Quetzalli-vdSZvpjxDXY.mp3"):
        #     print(score)
        #     print(recording_id)
        #     print(title)
        #     print(artist)
        infoOptions = {
            'simulate': True,
        }
        downloadMusicOptions = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        stream = open("podcasts.yml", "r")
        docs = yaml.safe_load_all(stream)
        totalFileSizes = 0
        for doc in docs:
            for key, value in doc.items():
                youtubeEntity = YoutubeEntity("https://www.youtube.com/playlist?list=PL-6ISBgjHD2GqZ4O2P8422CQulhUPwbC8", "non",
                                              3, 5)
                with youtube_dl.YoutubeDL(downloadMusicOptions) as ydlInfo:
                    playList = ydlInfo.extract_info(youtubeEntity.url)
                    # print(playList)
                    video_url = playList.get("url", None)
                    video_id = playList.get("id", None)
                    video_title = playList.get('title', None)
                    tracks = playList.get("entries")

