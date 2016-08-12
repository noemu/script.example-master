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



class PlayerWindow(xbmcgui.WindowXML):
    LABEL_ARTIST = 802
    LABEL_TITEL = 801
    LABEL_ALBUM = 803
    IMG_ALBUM = 800
    SLIDER_VOL = 815
    BUTTON_SHUFFLE = 817
    BUTTON_SHUFFLE_ACT = 818
    
    BUTTON_REPEAT = 819
    BUTTON_REPEAT_ACT = 819
    
    BUTTON_BACK = 809
    BUTTON_PLAY = 811
    BUTTON_PAUSE = 812
    BUTTON_FOR = 813
    BUTTON_VOL_UP = 816
    BUTTON_VOL_DOWN = 814
    def __init__(self, *args, **kwargs): 
        self.isRunning = True

        self.volume = 100

        


    def onAction(self , action):
        ACTION_PREVIOUS_MENU = 10
        ACTION_NAV_BACK = 92
        ACTION_UP = 3
        ACTION_DOWN = 4
        ACTION_LEFT = 1
        ACTION_RIGHT = 2
        ACTION_MIDDLE = 7
        
        ACTION_PAUSE = 12
        ACTION_STOP = 13
        ACTION_NEXT_ITEM = 14
        ACTION_PREV_ITEM = 15
        
        ACTION_FORWARD = 16
        ACTION_REWIND = 17
        ACTION_PLAYER_FORWARD = 77
        ACTION_PLAYER_REWIND = 78

        ACTION_PLAYER_PLAY = 79
        ACTION_VOLUME_UP = 88
        ACTION_VOLUME_DOWN = 89
        ACTION_MUTE = 91
        
        ACTION_PAGE_UP = 5 
        ACTION_PAGE_DOWN = 6  

        

        
        #ids = str(action.getId())
        
        #xbmc.log(ids)
        
        if (action == ACTION_PREVIOUS_MENU) or (action == ACTION_NAV_BACK):
            xbmcgui.Window(10000).setProperty("spotify-closed-by-user","true")
            self.isRunning = False
            self.close()
            

        if (action == ACTION_LEFT) or (action == ACTION_RIGHT):
            self.volSlider = self.getControl(self.SLIDER_VOL)
            volume = self.volSlider.getPercent()
            setVol(volume)
                
        if(action == ACTION_PLAYER_PLAY) or (action == ACTION_PAUSE):
            if(self.playing):
                getSite(pause)
                
            else:
                getSite(play)
                
                
                
        if (action == ACTION_VOLUME_UP):
            self.volume = self.volume + 3
            if(self.volume > 100):
                self.volume = 100
            setVol(self.volume)
            self.volSlider = self.getControl(self.SLIDER_VOL)
            self.volSlider.setPercent(self.volume)
                
        if (action == ACTION_VOLUME_DOWN):
            self.volume = self.volume- 3
            if(self.volume < 0):
                self.volume = 0
            setVol(self.volume)
            self.volSlider = self.getControl(self.SLIDER_VOL)
            self.volSlider.setPercent(self.volume)
        
        if (action == ACTION_FORWARD) or (action == ACTION_PLAYER_FORWARD) or (action == ACTION_NEXT_ITEM) or (action == ACTION_PAGE_UP):
            getSite(next)
            
        if (action == ACTION_REWIND) or (action == ACTION_PLAYER_REWIND) or (action == ACTION_PREV_ITEM) or (action == ACTION_PAGE_DOWN):
            getSite(prev)
            
        if(action == ACTION_STOP):
            getSite(pause)
            
            
            
    def onClick(self, controlID):
                
        if (controlID == self.BUTTON_PAUSE) or (controlID == self.BUTTON_PLAY):
            if(self.playing):
                getSite(pause)                
            else:
                getSite(play)      
                
        if (controlID == self.BUTTON_VOL_UP):
            self.volume = self.volume + 3
            if(self.volume > 100):
                self.volume = 100
            setVol(self.volume)
            self.volSlider = self.getControl(self.SLIDER_VOL)
            self.volSlider.setPercent(self.volume)
                
        if (controlID == self.BUTTON_VOL_DOWN):
            self.volume = self.volume- 3
            if(self.volume < 0):
                self.volume = 0
            setVol(self.volume)
            self.volSlider = self.getControl(self.SLIDER_VOL)
            self.volSlider.setPercent(self.volume)
        
        if (controlID == self.BUTTON_FOR):
            getSite(next)
            
        if (controlID == self.BUTTON_BACK):
            getSite(prev)
            
    
    def updateLabels(self, information):
        self.albumCover = self.getControl(self.IMG_ALBUM)
        self.titleLabel = self.getControl(self.LABEL_TITEL)
        self.artistLabel = self.getControl(self.LABEL_ARTIST)
        self.albumName = self.getControl(self.LABEL_ALBUM)
        self.volSlider = self.getControl(self.SLIDER_VOL)
    
    
        self.playing = information['playing']

        
        self.titleLabel.setLabel(information['track_name'])
        self.albumName.setLabel(information['album_name'])
        self.artistLabel.setLabel( information['artist_name'])
        self.albumCover.setImage(information['cover_url'])
        self.volume = int(information['volume'])/655.35
        self.volSlider.setPercent(self.volume)
        
        self.getControl(self.BUTTON_PLAY).setVisible(not self.playing)
        self.getControl(self.BUTTON_SHUFFLE).setVisible(not information['shuffle'])
        self.getControl(self.BUTTON_REPEAT).setVisible(not information['repeat'])


def getSite(url):
    #try...
    rq = requests.get(url)
    #handle
    return rq

def getInfo():
    information = getSite(info).json()
    
    statusInfo = getSite(status).json()
    
    
    playing = statusInfo['playing']
    shuffleInfo = statusInfo['shuffle']
    repeatInfo = statusInfo['repeat']
    
    coverURL = "http://o.scdn.co/160/"+information['cover_uri'].split(':')[-1]
    information['cover_url'] = coverURL
    information['playing'] = playing
    information['shuffle'] = shuffleInfo
    information['repeat'] = repeatInfo
    
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
    
    while True:
        try:
            window.getControl(800)
            break
        except Exception:            
            xbmc.log("Error: can't find Window, try again")
            time.sleep(1) # maybe fix for can't find window id's


    while window.isRunning and (not xbmc.abortRequested):
        information = getInfo()
        window.updateLabels(information)
        time.sleep(updateInterval)
        screensaverCount = screensaverCount + updateInterval
        
        if(screensaverCount>screensaverDelay) and information['playing']:
            #wakeup from screensaver by simulating a button activity
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Input.ContextMenu", "id": 1}')
            screensaverCount = 0

def main():
    pw = PlayerWindow("player.xml",CWD)

    
    #xbmcgui.Window( 10000 )

    t1 = Thread(target=updateInfo,args=("1",pw))
    t1.setDaemon( True)
    t1.start()
    
    xbmcgui.Window(10000).setProperty("spotify-showing", "true")
    
    pw.doModal()
    xbmcgui.Window(10000).clearProperty("spotify-showing")
    del t1
    del pw
    


    

if __name__ == '__main__':
    page = 'http://127.0.0.1:4000'
    apiPlayback = '/api/playback'
    
    play = page+apiPlayback+'/play'
    pause = page+apiPlayback+'/pause'
    prev = page+apiPlayback+'/prev'
    next = page+apiPlayback+'/next'
    volume = page+apiPlayback+'/volume'
    shuffle =  page+apiPlayback+'/shuffle'
    repeat =  page+apiPlayback+'/repeat'
    
    
    info = page+'/api/info/metadata'
    status = page+'/api/info/status'
    
    
    ADDON = xbmcaddon.Addon(id='plugin.audio.example')
    CWD = ADDON.getAddonInfo('path').decode("utf-8")



    main()
