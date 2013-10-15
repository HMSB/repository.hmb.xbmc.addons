#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import sys
import re
import os
import datetime
import xbmcplugin
import xbmcgui
import xbmcaddon
import string

socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
thumbsDir = xbmc.translatePath('special://home/addons/'+addonID+'/resources/thumbs')
forceViewMode = addon.getSetting("forceViewMode") == "true"
useThumbAsFanart = addon.getSetting("useThumbAsFanart") == "true"
autoPlay = int(addon.getSetting("autoPlay"))
viewModeNewsShows = str(addon.getSetting("viewModeNewsShows"))
viewModeVideos = str(addon.getSetting("viewModeVideos"))
prefRes = addon.getSetting("prefRes")
prefRes = [1080, 720, 520, 480, 360, 240][int(prefRes)]
itemsPerPage = addon.getSetting("itemsPerPage")
itemsPerPage = ["25", "50", "75", "100"][int(itemsPerPage)]
iconPathShows = os.path.join(thumbsDir, "shows.jpeg")
iconPath_AnimeMovie = os.path.join(thumbsDir, "anime.jpeg")
iconPathMost_watched = os.path.join(thumbsDir, "top5.jpeg")
iconPathMore = os.path.join(thumbsDir, "more.jpeg")
iconPathAtoZ = os.path.join(thumbsDir, "AtoZ.png")
urlShows = "http://okanime.com/category/anime/page/1/" 
urlAtoZ = "http://okanime.com/letter/A/?orderby=title"
urlMovies = "http://okanime.com/category/movie/page/1/"
urlTop5 = "http://okanime.com/category/anime/page/1/"

def index(): 
    addDir("Latest Items اخر الإضافات", urlShows, 'listShows', iconPathShows)
    addDir("A-Z الترتيب الأبجدي", urlAtoZ, 'ListAtoZ', iconPathAtoZ)
    addDir("Anime Movies افلام الانمي",urlMovies, 'listShows', iconPath_AnimeMovie)
    addDir("Top 5افضل ٥ انميات ", urlTop5, 'listShowsTop5', iconPathMost_watched)   
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def ListAtoZ(url):
    listAtoZ = string.uppercase[:26]
    i = 0
    while i< 26:
        addDir(listAtoZ[i], "http://okanime.com/letter/"+listAtoZ[i] +"/page/1/", 'listShows',os.path.join(thumbsDir,listAtoZ[i] + ".png" )  )
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listShowsTop5(url):
    htmlfile = urllib.urlopen(url)
    htmltext1 = htmlfile.read()
    htmltext = re.sub(r'^(.|\n)*<img src="http://okanime.com/images/widget-stars.png', '', htmltext1, re.S)
    regex1 = '''<a href="http://okanime.com/'''+'''[^,/]*/"'''+''' title="(.*?)">\n'''
    regex2 = '''<img src="(.*?)" width="'''
    regex3 = '''<a href="http://okanime.com/(.*?)/" class="post-title"'''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    showID = re.findall(pattern3,htmltext)
    i = 0
    while i< len(show_name):
        addDir(show_name[i], showID[i], 'listEpsodes', img_path[i])
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)
        
def listShows(url):
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    htmltext = re.sub(r'<img src="http://okanime.com/images/widget-stars.png(.|\n)*$', '', htmltext, re.S)
    htmltext = re.sub("&#(\d+)(;|(?=\s))", '', htmltext)
    regex1 = '''<a href="http://okanime.com/'''+'''[^,/]*/"'''+''' title="(.*?)">\n'''
    regex2 = '''<img src="(.*?)" alt="'''
   # regex3 = '''class="post-([0-9]*?) post type-post status-'''
    regex3 = '''<span class="page-title2"><a href="http://okanime.com/(.*?)/" title="'''
    regex4 = '''/page/(.*?)/'''
    regex5 = '''<a href="http://okanime.com/episodes/(.*?)/" rel="tag">'''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    pattern4 = re.compile(regex4)
    pattern5 = re.compile(regex5)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    showID = re.findall(pattern3,htmltext)
    pageNum = re.findall(pattern4,url)
    numOfEpisodes = re.findall(pattern5,htmltext)
    i = 0
    while i< len(show_name):
        addDir(show_name[i], showID[i], 'listEpsodes', img_path[i])
        i+=1
    pageCount = int(pageNum[0]) + 1
    url = re.sub("/page/.*","/page/"+str(pageCount)+"/", url)
    addDir("More", url, 'listShows', iconPathMore)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listEpsodes(showID):
    #numOfEpisodes = 26
   # urlCh = "http://okanime.com/?post_type=episode&p=" + str(int(showID)+14)
    urlCh = "http://okanime.com/" + showID
    htmlfile = urllib.urlopen(urlCh)
    htmltext = htmlfile.read()
    regex1 = '''p=(.*?)"'''
    pattern1 = re.compile(regex1)
    episodeID = re.findall(pattern1,htmltext)  
    if  len(episodeID)<1:
        showMessage("No Episodes Yet", "لم تتم الإضافة بعد","")
        numOfEpisodes = []
        i = 1000
    else:
        urlCh = "http://okanime.com/?post_type=episode&p=" + episodeID[0]
        htmlfile = urllib.urlopen(urlCh)
        htmltext = htmlfile.read()
        regex1 = '''/?cat=(.*?)"'''
        pattern1 = re.compile(regex1)
        showID2 = re.findall(pattern1,htmltext)
        urleps = "http://okanime.com/episode/?cat=" + showID2[0]
        htmlfile = urllib.urlopen(urleps)
        htmltext = htmlfile.read()
        regex1 = '''(.*?) الحلقة'''
        regex2 = '''p=(.*?)"'''
        pattern1 = re.compile(regex1)
        pattern2 = re.compile(regex2)
        numOfEpisodes = re.findall(pattern1,htmltext) 
        episodeID = re.findall(pattern2,htmltext) 
        i = 0  
    while i< len(numOfEpisodes):
        addLink("الحلقة " + str(i+1), "http://okanime.com/?post_type=episode&p=" + episodeID[i], 'playVideo', '', 'Plot', 000, 'date', str(i))
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)


def playVideo(url):
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    regex1 = '''<a href=(.*?) target=FRAME1 class="stream-link">google</a>'''
    pattern1 = re.compile(regex1)
    ch_name = re.findall(pattern1,htmltext)
    regex1 = '''http://okanime.com/player/google/.(.*?)&'''
    pattern1 = re.compile(regex1)
    videoList = re.findall(pattern1,ch_name[0])
    url = "http://docs.google.com/file/d/" + videoList[0] + "/preview"
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    regex3 = '''url=(.*?)&type='''
    pattern3 = re.compile(regex3)
    urlVideo = re.findall(pattern3,htmltext)
    video_path = urllib.unquote_plus(urlVideo[0])
    #video_path = "https://r8---sn-cg07luee.c.docs.google.com/videoplayback?requiressl=yes&shardbypass=yes&cmbypass=yes&id=aaccf970a874fed4&itag=35&source=webdrive&app=docs&ip=86.51.182.21&ipbits=0&expire=1381685119&sparams=requiressl,shardbypass,cmbypass,id,itag,source,ip,ipbits,expire&signature=245774BC5AC2C3F56BD44EDA398A23A521251C3A.8209C9759524F29ABDE2D216736AFCB3D5B85D4C&key=ck2&ir=1&ms=tsu&mt=1381681455&mv=m"
    listitem = xbmcgui.ListItem(path=video_path)
    #listitem.setInfo(type="Video", infoLabels={ "plot": desc})
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

    
def addLink(name, url, mode, iconimage, desc, length="", date="", nr=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc, "Aired": date, "Episode": nr})
    if length:
        liz.addStreamInfo('video', {'duration': int(length)})
    liz.setProperty('IsPlayable', 'true')
    if useThumbAsFanart:
        liz.setProperty("fanart_image", iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok
   
    
def showMessage(msg1,msg2, msg3):
        __addon__       = xbmcaddon.Addon()
        __addonname__   = __addon__.getAddonInfo('name')
        #xbmc.executebuiltin('Notification(%s, 50000)'%(msg))
        xbmcgui.Dialog().ok(__addonname__, msg1, msg2, msg3)
        
def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def addDir(name, url, mode, iconimage, type="", desc=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
type = urllib.unquote_plus(params.get('type', ''))

if mode == 'playVideo':
    playVideo(url)    
elif mode == 'listEpsodes':
    listEpsodes(url)
elif mode == 'listShows':
    listShows(url)
elif mode == 'listShowsTop5':
    listShowsTop5(url)
elif mode == 'listShowsTop5':
    ListAtoZ(url)
elif mode == 'showMessage':
    showMessage('Coming Soon','','')
else:
    index()

