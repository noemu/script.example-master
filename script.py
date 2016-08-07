import os
import sys
import urllib
import urlparse
import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
from threading import Thread
import time



def main():
    monitor = xbmc.Monitor()


    isPlaying = False;


            

    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            break
        
        try:
            info = requests.get(status)
            isPlaying = info.json()['playing']
        except requests.exceptions.RequestException as e:
            xbmc.sleep(10)
        else:
            xbmc.sleep(10)
            
        try:
            started = xbmcgui.Window(10000).getProperty("spotify-showing") == u'true'
        except ValueError as e:
            started = False
        if(isPlaying) and not started:
            xbmc.executebuiltin('RunAddon("plugin.audio.example")')
        xbmc.sleep(2)
        xbmc.log("sc: " + str(not(xbmcgui.Window(10000).getProperty("spotify-showing") == 'true'))+" isPlay: "+str(isPlaying))


    

if __name__ == '__main__':
    xbmc.log("spotify connect checker started")
    page = 'http://127.0.0.1:4000'

    status = page+'/api/info/status'


    main()