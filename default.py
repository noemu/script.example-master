# https://docs.python.org/2.7/
import os
import sys
import urllib
import urlparse
# http://mirrors.kodi.tv/docs/python-docs/

import xbmcaddon
import xbmcgui
import xbmcplugin
# http://docs.python-requests.org/en/latest/
import requests
from threading import Thread
import time



class PlayerWindow(xbmcgui.Window):
    def __init__(self): 
        self.isRunning = True

        self.albumCover = xbmcgui.ControlImage(300,300,200,200, '/tmp/spotAlCov.png')
        self.titleLabel = xbmcgui.ControlLabel(550, 300, 400, 50,"title", textColor='0xFFFFFFFF',font = 'font20')
        self.artistLabel = xbmcgui.ControlLabel(550, 380, 400, 50,"artist", textColor='0xFFFFFFFF',font = 'font13')
        self.albumName = xbmcgui.ControlLabel(550, 460, 400, 50,"title", textColor='0xFFFFFFFF',font = 'font13')
        
        
        self.addControl(self.albumCover)
        self.addControl(self.titleLabel)
        self.addControl(self.artistLabel)
        self.addControl(self.albumName)
        self.volume = 100

        


    def onAction(self , action):
        ACTION_PREVIOUS_MENU = 10
        ACTION_NAV_BACK = 92
        ACTION_UP = 3
        ACTION_DOWN = 4
        ACTION_LEFT = 1
        ACTION_RIGHT = 2
        ACTION_MIDDLE = 7

        #ids = str(action.getId())
        
        #xbmc.log(ids)
        
        if (action == ACTION_PREVIOUS_MENU) or (action == ACTION_NAV_BACK):
            self.isRunning = False
            self.close()
            
        if (action == ACTION_UP):
            self.volume = self.volume + 5
            if(self.volume > 100):
                self.volume = 100
            setVol(self.volume)
                
        if (action == ACTION_DOWN):
            self.volume = self.volume- 5
            if(self.volume < 0):
                self.volume = 0
            setVol(self.volume)
        
        if (action == ACTION_RIGHT):
            getSite(next)
            
        if (action == ACTION_LEFT):
            getSite(prev)
            
        if(action == ACTION_MIDDLE):
            if(self.playing):
                getSite(pause)
            else:
                getSite(play)
            
            

    def updateLabels(self, information):
        self.playing = information['playing']
        self.titleLabel.setLabel(information['track_name'])
        self.albumName.setLabel(information['album_name'])
        self.artistLabel.setLabel( information['artist_name'])
        self.albumCover.setImage(information['cover_url'])
        self.volume = int(information['volume'])/655.35


def getSite(url):
    #try...
    rq = requests.get(url)
    #handle
    return rq

def getInfo():
    information = getSite(info).json()
    playing = getSite(status).json()['playing']
    coverURL = "http://o.scdn.co/160/"+information['cover_uri'].split(':')[-1]
    information['cover_url'] = coverURL
    information['playing'] = playing
    return information

def downloadCover(url):
    urllib.urlretrieve(url,'/tmp/spotAlCov.png')

def setVol(value):
    value = int(round(value* 655.35))
    jsonPost = {'value': value}
    requests.post(volume,data=jsonPost)

def updateInfo(name,window):
    screensaverDelay = 30
    screensaverCount = 0
    updateInterval = 2


    while window.isRunning and (not xbmc.abortRequested):
        information = getInfo()
        window.updateLabels(information)
        time.sleep(updateInterval)
        screensaverCount = screensaverCount + updateInterval
        
        if(screensaverCount>screensaverDelay):
            #wakeup from screensaver by simulating a button activity
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Input.ContextMenu", "id": 1}')
            screensaverCount = 0

def main():
    pw = PlayerWindow()

    
    xbmcgui.Window( 10000 )

    t1 = Thread(target=updateInfo,args=("1",pw))
    t1.setDaemon( True)
    t1.start()
    
    xbmcgui.Window(10000).setProperty("spotify-showing", "true")
    
    pw.doModal()
    xbmcgui.Window(10000).clearProperty("spotify-showing")
    del pw
    del t1


    

if __name__ == '__main__':
    page = 'http://127.0.0.1:4000'
    apiPlayback = '/api/playback'
    
    play = page+apiPlayback+'/play'
    pause = page+apiPlayback+'/pause'
    prev = page+apiPlayback+'/prev'
    next = page+apiPlayback+'/next'
    volume = page+apiPlayback+'/volume'
    info = page+'/api/info/metadata'
    status = page+'/api/info/status'
    



    main()
