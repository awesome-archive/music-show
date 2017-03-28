# -*- coding: utf-8 -*-
 
#from django.http import HttpResponse
from django.shortcuts import render
import sqlite3

def show(request):
    context          = {}
    context['test'] = 'test!'
    return render(request, 'show.html', context)

def get_user_list(request):
    conn = sqlite3.connect('/Users/Mashaz/Github/django-test/music_show/user.db')
    cur = conn.cursor()
    cur.execute('SELECT uname FROM lastWeekRanking where rank=1')
    #message = [row[0] for row in cur.fetchall()]
    username_list = [] 
    for row in cur.fetchall():
        username_list.append(row[0])

    conn.close()
    context          = {}
    context['username_list'] = username_list
    return render(request, 'show.html', context)