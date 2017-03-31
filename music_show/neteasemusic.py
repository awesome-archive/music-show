# -*- coding:utf-8 -*-

import requests
import re
import os
import sys
import time
import random
import json
import sqlite3
import gb2260
from bs4 import BeautifulSoup
from collections import Counter


'''
username=修车 singer=unknown
'''
def UserSearch(username):

    url = 'http://music.163.com/api/search/get?s='+str(username)+'&type=1002&offset=0&limit=60'
    respo = requests.post(url)
    return  respo.content  #json

class NeteaseSpider:
	def GetPlayListDetail(self,plid):
		songList = []
		singerList = []
		url = 'http://music.163.com/playlist?id='+str(plid)
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
		respo = requests.get(url,headers=headers)
		soup = BeautifulSoup(respo.content)
		main = soup.find('ul',{'class':'f-hide'})
		
		for music in main.findAll('a'):
		    songList.append(music.text)
		    #print music.text
		
		singermain  = soup.find('textarea',{'style':'display:none;'})
		xxx = str(singermain.contents[0]).lstrip("u'").rstrip("'")
		try:
		    d = json.loads(xxx)
		    for i in range(0,len(d)):
		        singerList.append(d[i]['artists'][0]['name'])
		except:
		    for i in range(0,len(songList)):
		        singerList.append("unknown")
		return songList

	def UsernameInput(self,username):
		try:
		    nameJson = UserSearch(username)
		    d = json.loads(nameJson)
		    try:
		        myname = d['result']['userprofiles'][0]['nickname']
		    except:
		        return 'error'
		    myid = d['result']['userprofiles'][0]['userId']
		    return myid
		except Exception ,e :
		    return 'error'

	def GetAllListId(self,uid):

		url = 'http://music.163.com/user/home?id='+str(uid)
		respo = requests.get(url)
		re_count = re.compile(r'cCount:[0-9]{1,3},')
		ccount = int(re.findall(re_count,respo.content)[0].lstrip('cCount:').rstrip(',')) #创建的歌单数

		offset=0
		limit=100
		url = 'http://music.163.com/api/user/playlist/?offset={}&limit={}&uid={}'.format(offset,limit,uid)
		'''
		为csrf_token搞了大半天，感谢github上的musicbox项目,上了api,但api次数太少会被ban
		'''
		respo = requests.get(url)
		print '获得歌单list,解析中...'
		re_id = re.compile(r'\"id\":[0-9]{6,9}\D')
		idlist = re.findall(re_id,respo.content)
		name_list = []
		for i in range(0,len(idlist)):
		    idlist[i] = idlist[i].lstrip('"id":').rstrip('}').rstrip(',')
		idlist = idlist[0:ccount]
		d = json.loads(respo.content)
		for i in range(0,ccount):
		    songname = d['playlist'][i]['name']
		    name_list.extend(songname)
		print '解析完毕'
		return  idlist   #创建的所有的歌单id列表
	def GetPlayListDetail(self,plid):

		songList = []
		singerList = []
		url = 'http://music.163.com/playlist?id='+str(plid)
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
		respo = requests.get(url,headers=headers)
		soup = BeautifulSoup(respo.content)
		main = soup.find('ul',{'class':'f-hide'})

		for music in main.findAll('a'):
		    songList.append(music.text)
		    #print music.text

		singermain  = soup.find('textarea',{'style':'display:none;'})
		xxx = str(singermain.contents[0]).lstrip("u'").rstrip("'")
		try:
		    d = json.loads(xxx)
		    for i in range(0,len(d)):
		        singerList.append(d[i]['artists'][0]['name'])
		except:
		    for i in range(0,len(songList)):
		        singerList.append("unknown")
		

		return songList,singerList


