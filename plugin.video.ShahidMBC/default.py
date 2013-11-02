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
import json
import xbmc

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
urlMain = "http://shahid.mbc.net"
iconPathChannels = os.path.join(thumbsDir, "channels.png")
iconPathWhats_new = os.path.join(thumbsDir, "whats_new.png")
iconPathMost_watched = os.path.join(thumbsDir, "most_watchd.png")
iconPathAtoZ = os.path.join(thumbsDir, "AtoZ.png")
urlBase = "http://shahid.mbc.net"
urlChannels = "http://shahid.mbc.net/media/channels"
urlSearch = "http://shahid.mbc.net/Ajax/seriesFilter?year=0&dialect=0&title=0&genre=0&channel=0&prog_type=0&media_type=0&airing=0&sort=alpha&series_id=0&offset=0&sub_type=0&limit=10000"
MBCproviderID = '2fda1d3fd7ab453cad983544e8ed70e4'

def index(): 
    addDir("Channles", "", 'listChannels', iconPathChannels)
    addDir("New Items", "http://shahid.mbc.net/media/episodes?sort=latest", 'listEpisodesSorted', iconPathWhats_new)
    addDir("Most Watched", "http://shahid.mbc.net/media/episodes?sort=popular_all", 'listEpisodesSorted', iconPathMost_watched)
    addDir("A-Z", urlSearch, 'listShowsSorted', iconPathAtoZ)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listChannels():
    htmlfile = urllib.urlopen(urlChannels)
    htmltext = htmlfile.read()
    regex1 = '''<li><a href="/media/channel/'''+'''[0-9]*'''+'''/(.+?)"'''
    regex2 = '''title=""><b><img src="(.+?)"'''
    regex3 = '''<a href="(.+?)" title='''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    ch_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(ch_name):
        addDir(ch_name[i], ch_path[i], 'listShows', img_path[i])
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listShows(ch_path):
    #urlCh = "http://shahid.mbc.net"+ ch_path
    chID = re.findall(re.compile('''/media/channel/(.*?)/'''),ch_path)
    urlCh = "http://shahid.mbc.net/Ajax/series_sort?offset=0&channel_id=" + chID[0] + "&sort=latest&limit=500"
    htmlfile = urllib.urlopen(urlCh)
    htmltext = htmlfile.read()
    regex1 = '''<span class="title major">(.+?)</span>'''
    regex2 = '''title=""><b><img src="(.+?)"'''
    regex3 = '''" href="(.*?)" title="">'''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(show_name):
        addDir(show_name[i], ch_path[i], 'listEpsodes', img_path[i])
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listShowsSorted(urlCh):
    htmlfile = urllib.urlopen(urlCh)
    htmltext = htmlfile.read()
    regex1 = '''<span class="title major">(.+?)</span>'''
    regex2 = '''title=""><b><img src="(.+?)"'''
    regex3 = '''" href="(.*?)" title="">'''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(show_name):
        addDir(show_name[i], ch_path[i], 'listEpsodes', img_path[i])
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listEpsodes(ch_path):
    #urlCh = ch_path
    #http://shahid.mbc.net/Ajax/episode/761?offset=10&media_type=program&limit=10&sort=season&season=null
    chID = re.findall(re.compile('''/media/program/(.*?)/'''),ch_path)
    urlCh = "http://shahid.mbc.net/Ajax/episode/" + chID[0] + "?offset=0&media_type=program&limit=5000&sort=season&season=null"
    htmlfile = urllib.urlopen(urlCh)
    htmltext = htmlfile.read()
    regex1 = '''</span><span class="title">(.*?)</span>'''
    regex2 = '''img src="(.*?)" alt="" border="0" height="" width=""'''
    regex3 = '''</span><a href="(.+?)" title='''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(show_name):
        addLink(show_name[i], ch_path[i], 'playVideo', img_path[i], 'Plot', 000, 'date', str(i))
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)

def listEpisodesSorted(urlCh):
  #  urlCh = "http://shahid.mbc.net/media/episodes?sort=latest"
    htmlfile = urllib.urlopen(urlCh)
    htmltext = htmlfile.read()
    regex1 = '''<a href="/media/video/(.*?)" title=""><b>'''
    regex2 = '''img src="(.*?)" alt="" border="0" height="" width=""'''
    regex3 = '''</span><a href="(.+?)" title='''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)
    show_name = re.findall(pattern1,htmltext)
    img_path = re.findall(pattern2,htmltext)
    ch_path = re.findall(pattern3,htmltext)
    i = 0
    while i< len(show_name):
        ep_name_print = re.sub( '_', ' ', show_name[i])
        ep_name_print = re.sub( '.*/', ' ', ep_name_print)
        addLink(ep_name_print, ch_path[i], 'playVideo', img_path[i], 'Plot', 000, 'date', str(i))
        i+=1
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewModeNewsShows+')')
    xbmcplugin.endOfDirectory(pluginhandle)


def videoInfo(ch_path):
    # extracting mediaID
    htmlfile = urllib.urlopen(urlBase + ch_path)
    htmltext = htmlfile.read()
    regex1 = '''mediaId=(.*?)&&default'''
    pattern1 = re.compile(regex1)
    mediaID = re.findall(pattern1,htmltext)    
    # obtaining rtmpURL
    urlContentProvider = 'http://production.ps.delve.cust.lldns.net/PlaylistService'
    headerValues = {'content-type' : 'text/soap+xml'}
    soapParm = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><SOAP-ENV:Body><tns:getPlaylistByMediaId xmlns:tns="http://service.data.media.pluggd.com"><tns:in0>''' + mediaID[0] + '''</tns:in0><tns:in1 xsi:nil="true"/></tns:getPlaylistByMediaId></SOAP-ENV:Body></SOAP-ENV:Envelope>'''
    full_url = urllib2.Request(urlContentProvider, data=soapParm, headers=headerValues)
    response = urllib2.urlopen(full_url)
    urlResponse = response.read()
    regex1 = '''</previewStream><url>(.*?)</url><videoBitRate>'''
    regex2 = '''<videoHeightInPixels>(.*?)</videoHeightInPixels>'''  
    regex3 = '''<description>(.*?)</description>'''
    pattern1 = re.compile(regex1)
    pattern2 = re.compile(regex2)
    pattern3 = re.compile(regex3)  
    rtmpURL = re.findall(pattern1,urlResponse)
    resolution = re.findall(pattern2,urlResponse)
    descList =  re.findall(pattern3,urlResponse)
    if  not descList:
        desc = 'Sorry, Shahid Has no Plot'
    else:
        desc = descList[0]
    videoProp = [rtmpURL, resolution, desc]
    return videoProp

def playVideo(ch_path):
    # selecting resolution
    videoProp = videoInfo(ch_path)
    rtmpURL =    videoProp[0]
    resolution = videoProp[1]
    desc = videoProp[2]
    resolution = map(int, resolution)
    if prefRes not in resolution:
        playResPos = resolution.index(max(resolution))
    elif prefRes > max(resolution):
        playResPos = resolution.index(max(resolution)) 
    else: 
        playResPos = resolution.index(prefRes)       
    # Play video
    rtmpURLfinal = re.sub("/v1/mp4:media", "/v1/ playpath=mp4:media",rtmpURL[playResPos])
    rtmpURLfinal = rtmpURLfinal + " pageURL=" + urlBase + ch_path + " swfUrl=http://s.delvenetworks.com/deployments/flash-player/flash-player-5.6.2.swf?ldr=ldr"
    #rtmpURLfinal = rtmpURLfinal + " pageURL=http://assets.delvenetworks.com/player/fp10loader.swf swfUrl=http://s.delvenetworks.com/deployments/flash-player/flash-player-5.6.2.swf?ldr=ldr"
    listitem = xbmcgui.ListItem(path=rtmpURLfinal)
 #   listitem = xbmcgui.ListItem(path="rtmpe://mbc3.csl.delvenetworks.com/a6344/v1/ playpath=mp4:media/2fda1d3fd7ab453cad983544e8ed70e4/bbccfbfd519648128f5fec290f2f74b3/78eb17d59e9a4ae3a4888fc85fd3a69e/still_standing_s01_e01_vod.mp4  pageURL=http://assets.delvenetworks.com/player/fp10loader.swf?allowEmbed=true&allowSharePanel=true&allowHttpDownload=&startQuality=200&mediaId=08e681cdd644444e8cedd2507d027a1a&autoplay=true&playerForm=64fc5d4a5f47400fac523fba125a8de8&deepLink=true&77926330 swfUrl=http://s.delvenetworks.com/deployments/flash-player/flash-player-5.6.2.swf?ldr=ldr")
 #   listitem = xbmcgui.ListItem(path=rtmpURL[playResPos])
    listitem.setInfo(type="Video", infoLabels={ "plot": desc})
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
elif mode == 'listShowsSorted':
    listShowsSorted(url)    
elif mode == 'listEpisodesSorted':
    listEpisodesSorted(url)    
elif mode == 'listEpsodes':
    listEpsodes(url)
elif mode == 'listShows':
    listShows(url)
elif mode == 'listChannels':
    listChannels()
elif mode == 'showMessage':
    showMessage('Coming Soon')
else:
    index()

