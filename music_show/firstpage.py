# -*- coding: utf-8 -*-
 
#from django.http import HttpResponse
from django.shortcuts import render
 
def first_page(request):
    return render(request, 'index.html')

def analysis_page(request):
	return render(request, 'analysis.html')

def compare_page(request):
	return render(request, 'compare.html')