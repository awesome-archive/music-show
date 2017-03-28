# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')   # note
# 表单
def search_form(request):
    return render_to_response('index.html')

def get_user_list():
    conn = sqlite3.connect('/Users/Mashaz/Github/django-test/music_show/user.db')
    cur = conn.cursor()
    cur.execute('SELECT uname FROM lastWeekRanking where rank=1')
    #message = [row[0] for row in cur.fetchall()]
    username_list = [] 
    for row in cur.fetchall():
        username_list.append(row[0])

    conn.close()
    return username_list

def get_all_song(username):
    conn = sqlite3.connect('/Users/Mashaz/Github/django-test/music_show/user.db')
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

def search(request):  
    request.encoding='utf-8'
    if 'username' in request.GET:
        search_key = request.GET['username'].encode('utf-8')
        if search_key =='':
            context = {}
            context['empty_flag'] = 'nothing';
            return render(request, 'show.html', context)
        else:
            song_list = get_all_song(search_key)
            if song_list != []:
                context = {}
                context['username_list'] = song_list
                return render(request, 'show.html', context)
            else:
                context = {}
                context['no_record'] = 'nothing';
                return render(request, 'show.html', context)