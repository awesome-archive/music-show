# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import neteasemusic 
import sqlite3
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')   # note



def analysis(request):
    if 'username' and 'isall' in request.GET: 
        search_key = request.GET['username'].encode('utf-8')
        sfile = open('username_log.txt','a')
        sfile.write(search_key)
        sfile.write('.all')
        sfile.write('\n')
        sfile.close()
        mspider = neteasemusic.NeteaseSpider()
        uid = mspider.UsernameInput(search_key)
        if uid == 'error':
            context = {}
            context['no_record'] = 'nothing';
            return render(request, 'show.html', context)
        else:
            all_playlist_id = mspider.GetAllListId(uid)
            all_list = []
            all_singer_list = []
            for playlist_id in all_playlist_id:
                song_list , singer_list = mspider.GetPlayListDetail(playlist_id)
                all_singer_list.extend(singer_list)
                for i in range(0,len(song_list)):
                    all_list.append(str(song_list[i]) + ' - ' + str(singer_list[i]))

            # song_list , singer_list = mspider.GetPlayListDetail(playlist_id)
            
            context = {}
            
            
            singer_info_list = mspider.singerAnalysis(all_singer_list)
            if singer_info_list != 'error':
                singer_list = []
                times_list = []
                for i in singer_info_list:
                    s = []
                    s = i.split('--')
                    singer_list.append(s[0].strip())
                    times_list.append(s[1].strip())
           
                # context['singer_list'] = singer_list
                # context['times_list'] = times_list
                # return render(request, 'show.html', context)
                return render(request, 'show.html', {
                    'singer_list': json.dumps(singer_list),
                    'times_list': json.dumps(times_list) })
            else:
                pass

    else:

        search_key = request.GET['username'].encode('utf-8')
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
            
            singer_info_list = mspider.singerAnalysis(singer_list)
            if singer_info_list != 'error':
                singer_list = []
                times_list = []
                for i in singer_info_list:
                    s = []
                    s = i.split('--')
                    singer_list.append(s[0].strip())
                    times_list.append(s[1].strip())
           
                # context['singer_list'] = singer_list
                # context['times_list'] = times_list
                # return render(request, 'show.html', context)
                return render(request, 'show.html', {
                    'singer_list': json.dumps(singer_list),
                    'times_list': json.dumps(times_list) })
            else:
                pass





   