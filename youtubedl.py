from __future__ import unicode_literals
import youtube_dl
import yaml

from youtubeEntity import YoutubeEntity

class YoutubeDL:


    def __init__(self):
        self.y = "y"

    def get(self):
        infoOptions = {
            'simulate': True,
        }
        downloadMusicOptions = {
            'format': 'bestaudio/best',
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
                with youtube_dl.YoutubeDL(infoOptions) as ydlInfo:
                    playList = ydlInfo.extract_info(youtubeEntity.url)
                    print(playList)
                    video_url = playList.get("url", None)
                    video_id = playList.get("id", None)
                    video_title = playList.get('title', None)
                    tracks = playList.get("entries")
                    for track in tracks:
                        print("Title %s " % track["title"])
                        print("URL %s " % track["webpage_url"])
                        with youtube_dl.YoutubeDL(downloadMusicOptions) as ydlMusic:
                            ydlMusic.download([track["webpage_url"]])
                            # formats_ = track['formats']
                            # for fr in formats_:
                            #     print(fr['ext'])
                            #     if fr['ext'] == 'webm':
                            #         totalFileSizes += fr['filesize']
                    print("Size %s Gb" % (totalFileSizes) )
                    return
        # print("Track %s " % track)


