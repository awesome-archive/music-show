# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import neteasemusic 
import sqlite3
import sys
import os
import time
import platform
import json
from django.http import StreamingHttpResponse

reload(sys)
sys.setdefaultencoding('utf-8')   # note
# 表单
def search_form(request):
    return render_to_response('index.html')

'''
from db
'''
def get_user_list():
    conn = sqlite3.connect('/Users/Mashaz/Github/django-test/music-show/user.db')
    cur = conn.cursor()
    cur.execute('SELECT uname FROM lastWeekRanking where rank=1')
    #message = [row[0] for row in cur.fetchall()]
    username_list = [] 
    for row in cur.fetchall():
        username_list.append(row[0])

    conn.close()
    return username_list


def get_all_song(username):
    conn = sqlite3.connect('/Users/Mashaz/Github/django-test/music-show/user.db')
    cur = conn.cursor()
    #uname=%s'%(username)
    query_string = "SELECT song FROM allTimeRanking where uname='%s'"%(str(username))
    print query_string
    cur.execute(query_string)
    #message = [row[0] for row in cur.fetchall()]
    song_list = []
    for row in cur.fetchall():
        song_list.append(row[0])

    conn.close()
    return song_list
# 接收请求数据

def export2kgl(request):
    search_key = request.session.get('search_key',default=None)
    system_info = platform.system()
    if system_info == 'Darwin':
        with open('/Users/Mashaz/Github/kgl-files/%s.kgl'%(search_key)) as f:
            c = f.read()
    else:
        with open('/root/kgl_files/%s.kgl'%(search_key)) as f:
            c = f.read()
    return HttpResponse(c)
   

def convert2kgl(search_key,all_list):
    system_info = platform.system()
    if system_info == 'Darwin':
        sfile = open('/Users/Mashaz/Github/kgl-files/%s.txt'%(search_key),'w')
    else:
        sfile = open('/root/kgl_files/%s.txt'%(search_key),'w')
    
    kgl_start = '<?xml version="1.0" encoding="utf-8"?>'
    sfile.write(kgl_start)
    sfile.write('\n')

    sfile.write('<List ListName="导入的列表">')
    sfile.write('\n')
    print len(all_list)
    for song in all_list:
        songs = song.split('-')
        song = str(songs[1]).strip() + ' - ' + str(songs[0]).strip() + '.mp3'
        song_sentence = '<FileName>'+ str(song.strip())+'</FileName>'
        sfile.write(song_sentence)
        sfile.write('\n')
    sfile.close()

    
    if system_info == 'Darwin':
        excute_s = 'mv /Users/Mashaz/Github/kgl-files/'+str(search_key)+'.txt /Users/Mashaz/Github/kgl-files/'+str(search_key)+'.kgl'
    else:
        
        excute_s = 'mv /root/kgl_files/'+str(search_key)+'.txt /root/kgl_files/'+str(search_key)+'.kgl'
    os.system(excute_s)

def compare(request):
    request.encoding='utf-8'
    if 'username1' and 'username2' in request.GET:

        search_key1 = request.GET['username1'].encode('utf-8')
        search_key2 = request.GET['username2'].encode('utf-8')
        sfile = open('username_log.txt','a')
        sfile.write(search_key1)
        sfile.write('\n')
        sfile.write(search_key2)
        sfile.write('\n')
        sfile.close()
        mspider = neteasemusic.NeteaseSpider()
        uid1 = mspider.UsernameInput(search_key1)
        uid2 = mspider.UsernameInput(search_key2)


        if uid1 == 'error' or uid2 == 'error':
            context = {}
            context['no_record'] = 'nothing';
            return render(request, 'show.html', context)
        else:
            if 'isall' in request.GET:
                is_all = request.GET['isall'].encode('utf-8')
                pass
            else:
                playlist1_id = mspider.GetAllListId(uid1)[0]
                playlist2_id = mspider.GetAllListId(uid2)[0]
                iLikeSongList,iSingerList = mspider.GetPlayListDetail(playlist1_id) #playlist id not user id
                time.sleep(0.5)
                uLikeSongList,uSingerList = mspider.GetPlayListDetail(playlist2_id)
                num_list , sameSongList = mspider.compare(iLikeSongList,iSingerList,uLikeSongList,uSingerList)
    
                final_sentence = str(search_key1)+'列表有'+str(num_list[0])+'首歌,'+str(search_key2)+'列表有'+str(num_list[1])+'首歌'
                
                #iSingerList  uSingerList
                singer_info_list = mspider.singerAnalysis(iSingerList)
                if singer_info_list != 'error':
                    singer_list = []
                    times_list = []
                    for i in singer_info_list:
                        s = []
                        s = i.split('--')
                        singer_list.append(s[0].strip())
                        times_list.append(s[1].strip())
                
                singer_info_list2 = mspider.singerAnalysis(uSingerList)
                if singer_info_list2 != 'error':
                    singer_list2 = []
                    times_list2 = []
                    for i in singer_info_list2:
                        s = []
                        s = i.split('--')
                        singer_list2.append(s[0].strip())
                        times_list2.append(s[1].strip())
            
    
                context = {}
                context['singer_list'] = json.dumps(singer_list)
                context['times_list'] = json.dumps(times_list)
                context['singer_list2'] = json.dumps(singer_list2)
                context['times_list2'] = json.dumps(times_list2)
                context['final_sentence'] = final_sentence
                context['sameSongList'] = sameSongList
    
                return render(request, 'show.html', context)

    else:
        context = {}
        context['empty_flag'] = 'nothing';
        return render(request, 'show.html', context)
def search(request):  
    request.encoding='utf-8'
    if 'username' and 'username2' in request.GET:
        pass

    elif 'username' and 'isall' in request.GET:  # 输出所有歌单
    
        search_key = request.GET['username'].encode('utf-8')
        sfile = open('username_log.txt','a')
        sfile.write(search_key)
        sfile.write('.all')
        sfile.write('\n')
        sfile.close()
        mspider = neteasemusic.NeteaseSpider()
        uid = mspider.UsernameInput(search_key)
        is_all = request.GET['isall'].encode('utf-8')
        
        if uid == 'error':
            context = {}
            context['no_record'] = 'nothing';
            return render(request, 'show.html', context)
        else:
            all_playlist_id = mspider.GetAllListId(uid) #list
            all_list = []

            for playlist_id in all_playlist_id:
                song_list , singer_list = mspider.GetPlayListDetail(playlist_id)
                for i in range(0,len(song_list)):
                    all_list.append(str(song_list[i]) + ' - ' + str(singer_list[i]))
            
            context = {}
            context['song_list'] = all_list

            return render(request, 'show.html', context)

    elif 'username' in request.GET:   # 输出我的喜欢
        search_key = request.GET['username'].encode('utf-8')
        request.session['search_key'] = search_key

        sfile = open('username_log.txt','a')
        sfile.write(search_key)
        sfile.write('\n')
        sfile.close()

        mspider = neteasemusic.NeteaseSpider()
        uid = mspider.UsernameInput(search_key)
        if uid == 'error':
            context = {}
            context['no_record'] = 'nothing';
            return render(request, 'show.html', context)
        else:
            playlist_id = mspider.GetAllListId(uid)[0]
            song_list , singer_list = mspider.GetPlayListDetail(playlist_id)
            context = {}
            all_list = []
            for i in range(0,len(song_list)):
                all_list.append(str(song_list[i]) + ' - ' + str(singer_list[i]))
            convert2kgl(search_key,all_list)
            context['song_list'] = all_list

            return render(request, 'show.html', context)


