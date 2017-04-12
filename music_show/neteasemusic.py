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
bug report
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

	
	def singerAnalysis(self,singerList):

		word_counts = Counter(singerList)
		try:
			top_three = word_counts.most_common(10)
		except:
			top_three = word_counts.most_common(5)
		x = []
		singer_info_list = []
		for i in range(0,len(top_three)):
			x.append(top_three.pop()) 
			singer_info_list.append(str(x[i][0])+str('--')+str(x[i][1]))

		# try:
		# 	x1 = top_three.pop()
		# 	x2 = top_three.pop()
		# 	x3 = top_three.pop()
		# 	x4 = top_three.pop()
		# 	x5 = top_three.pop()
		# 	x6 = top_three.pop()
		# except:
		# 	return 'error'
		# singer_info_list = []
		# singer_info_list.append(str(x6[0])+str('--')+str(x6[1])) 
		# singer_info_list.append(str(x5[0])+str('--')+str(x5[1]))
		# singer_info_list.append(str(x4[0])+str('--')+str(x4[1]))
		# singer_info_list.append(str(x3[0])+str('--')+str(x3[1]))
		# singer_info_list.append(str(x2[0])+str('--')+str(x2[1]))
		# singer_info_list.append(str(x1[0])+str('--')+str(x1[1]))
		return singer_info_list

	def compare(self,iLikeSongList,iSingerList,uLikeSongList,uSingerList):

		for i in range(0,len(iLikeSongList)):
		    iLikeSongList[i] = iLikeSongList[i] + ' - ' + iSingerList[i]
		for i in range(0,len(uLikeSongList)):
		    uLikeSongList[i] = uLikeSongList[i] + ' - ' + uSingerList[i]

	
		print '------------------------------------------------------'
	
		#singerAnalysis(iSingerList,0)
		print '------------------------------------------------------'

		#singerAnalysis(uSingerList,0)
		sameSongList = []
		for isong in iLikeSongList:
		    for usong in uLikeSongList:
		        if str(isong) == str(usong):
		            sameSongList.append(isong)
		sameSongList = list(set(sameSongList))
	

		final_num = [len(iLikeSongList),len(uLikeSongList)]
		return final_num,sameSongList