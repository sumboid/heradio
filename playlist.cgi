#!/usr/bin/env python

import mpd
import json

print "Content-Type: text/plain;charset=utf-8"
print

mpdClient = mpd.MPDClient()
mpdClient.connect("192.168.0.9", 6600)

print json.dumps({"playlist" :
                   map(lambda x: (x["artist"],
                                  x["title"],
                                  str(int(x["time"]) / 60) + ":" + (lambda x : str(x) if x >= 10 else "0" + str(x))(int(x["time"]) % 60),
                                  x["pos"]),
                                  mpdClient.playlistinfo()),
                   "current" : mpdClient.currentsong()["pos"]})
