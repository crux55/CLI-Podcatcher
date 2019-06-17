"""
Delete all playlists from Plex using PlexAPI

https://github.com/mjs7231/python-plexapi
"""

from plexapi.server import PlexServer
import requests

baseurl = ''
token = ''
plex = PlexServer(baseurl, token)

tmp_lst = []
print(plex.library.section('Music').all())

for playlist in plex.library.sections():
    print(playlist.key)
    tmp = playlist.key
    split = tmp.split('/library/')
    tmp_lst += [split[1]]

for i in tmp_lst:
    print(i)
    try:
        r = requests.delete('{}/library/{}?X-Plex-Token={}'.format(baseurl,i,token))
        print(r)

    except Exception as e:
        print (e)
