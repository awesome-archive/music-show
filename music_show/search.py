# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import neteasemusic 
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')   # note
# 表单
def search_form(request):
    return render_to_response('index.html')

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
'''
'''
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
'''

def search(request):  
    request.encoding='utf-8'
    if 'username' and 'username2' in request.GET:
        # search_key = request.GET['username'].encode('utf-8')
        # search_key2 = request.GET['username2'].encode('utf-8')
        # if search_key =='':
        #     context = {}
        #     context['empty_flag'] = 'nothing';
        #     return render(request, 'show.html', context)
        # elif search_key2 == '' :
        #     username_list = get_all_song(search_key)
        #     if username_list != []:
        #         context = {}
        #         context['username_list'] = username_list
        #         return render(request, 'show.html', context)
        #     else:
        #         context = {}
        #         context['no_record'] = 'nothing';
        #         return render(request, 'show.html', context)
        pass

    elif 'username' and 'isall' in request.GET:  # 输出所有歌单

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
            context['song_list'] = all_list;

            return render(request, 'show.html', context)

    elif 'username' in request.GET:   # 输出我的喜欢
        search_key = request.GET['username'].encode('utf-8')
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
            context['song_list'] = all_list;

            return render(request, 'show.html', context)


