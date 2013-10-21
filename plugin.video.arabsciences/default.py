#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import sys
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon

REMOTE_DBG = False
# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)


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
iconPathIcon1 = os.path.join(thumbsDir, "icon1.png")
iconPathIcon2 = os.path.join(thumbsDir, "icon2.png")
iconPathIcon3 = os.path.join(thumbsDir, "icon3.png")
iconPathIcon4 = os.path.join(thumbsDir, "icon4.png")
urlMain = "http://www.arabsciences.com/"
url1 = "http://www.arabsciences.com/category/tv-channels/"
url2 = ""
url3 = ""
url4 = ""

def index(): 
    addDir("Channels قنوات البثّ", url1, 'listLevel11', iconPathIcon1)
    addDir("Level12 name", url2, 'listLevel12', iconPathIcon2)
    addDir("Level13 name", url3, 'listLevel13', iconPathIcon3)
    addDir("Level14 name", url4, 'listLevel14', iconPathIcon4)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listLevel11(url):
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    regex1 = '''<span class="wpmega-link-title">(.*?)</span>'''
    #regex2 = '''width="16" src="(.*?)" alt="'''
    regex3 = '''www.arabsciences.com/category/tv-channels/(.*?)/'''
    pattern1 = re.compile(regex1)
    pattern3 = re.compile(regex3)
    ch_name = re.findall(pattern1,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 1
    while ch_name[i]!="تصنيف البرامج":
        addDir(ch_name[i], url1 + ch_path[i+3]+"/page/1/", 'listLevelLast', os.path.join(thumbsDir, ch_name[i]+".jpeg"))
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listLevelLast(url):
    #http://www.arabsciences.com/category/tv-channels/natgeoad/page/2/
    #url = url1+video_path
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    htmltext = re.sub("&#(\d+)(;|(?=\s))", '', htmltext)
    regex1 = '''" title="(.*?)"></a>'''
    regex2 = '''<img width="180" height="135" src="(.*?)" class="attachment-post-thumbnail wp-post-image" alt="'''
    regex3 = '''" href="(.*?)" title="'''
    regex4 = '''/page/(.*?)/'''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    pattern4 = re.compile(regex4)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    video_path = re.findall(pattern3,htmltext)
    pageNum = re.findall(pattern4,url)
    i = 0
    while i< len(show_name):
        addLink(show_name[i], video_path[i], 'playVideo', img_path[i], 'Plot', 000, 'date', str(i))
        i+=1
    pageCount = int(pageNum[0]) + 1
    url = re.sub("/page/.*","/page/"+str(pageCount)+"/", url)
    addDir("More", url, 'listLevelLast', os.path.join(thumbsDir, "more.jpeg"))
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)


def playVideo(url):
    #url = "http://www.arabsciences.com/2013/06/26/%D8%A7%D9%84%D8%B2%D9%87%D8%B1%D8%A7%D9%88%D9%8A/"
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    #regex1 = '''file":"http.*://www.youtube.com/watch\?v=(.*?)"'''
    regex1 = '''http.*://www.youtube.com/watch\?v=(.*?)"|src="http://www.youtube.com/embed/(.*)\?'''
    regex2 = '''type="video/mp4" href="(.*?)"'''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    videoID1 = re.findall(pattern1,htmltext)
    videoID2 = re.findall(pattern2,htmltext)
    # Play video
    if len(videoID1)>0:
        videoID = filter(None, videoID1[0])[0]
        urlVideo = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + videoID
        url = "http://www.youtube.com/watch?v=" + videoID 
        htmlfile = urllib.urlopen(url)
        htmltext = htmlfile.read()
        regex4 = '''<meta name="description" content="(.*?)"'''
        pattern4 = re.compile(regex4)
        videoDesc = re.findall(pattern4,htmltext)
    else:
        urlVideo = videoID2[0]
        videoDesc = "No Plot"
    #urlVideo = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=H-WMIQLbpJA"
    # adding description
    
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    regex4 = '''<meta name="description" content="(.*?)"'''
    pattern4 = re.compile(regex4)
    videoDesc = re.findall(pattern4,htmltext)
    #print unicode(videoDesc[0], 'utf-8')
    listitem = xbmcgui.ListItem(path=urlVideo)
    listitem.setInfo(type="Video", infoLabels={ "plot": unicode(videoDesc[0], 'utf-8')})
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
    

def showMessage(msg):
        xbmc.executebuiltin('XBMC.Notification(%s, 5000)'%(msg)) 
        
def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

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
elif mode == 'listLevelLast':
    listLevelLast(url)
elif mode == 'listLevel11':
    listLevel11(url)
elif mode == 'showMessage':
    showMessage('Coming Soon')
else:
    index()

