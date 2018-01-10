#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from form.models import User,User_data,Code_data
from django.core.cache import cache

def get_readed_cache(key):
    if cache.has_key(key):
        return cache.get(key)
    else:
        return key

def home(request):
    return render(request, 'home.html')

def user_data(request):
    if get_readed_cache("User_datalist") == "User_datalist":
        User_datalist = User_data.objects.all()
    else:
        User_datalist= get_readed_cache("User_datalist")
        cache.set(key, User_datalist, 60 * 60)  # 设置有效期一小时,设置缓存
    return render(request, 'user_data.html',{'User_datalist':User_datalist})

def code_data(request):
    if get_readed_cache("Code_datalist") == "Code_datalist":
        Code_datalist = Code_data.objects.all()
    else:
        Code_datalist= get_readed_cache("Code_datalist")
        cache.set(key, Code_datalist, 60 * 60)  # 设置有效期一小时,设置缓存
    return render(request, 'code_data.html',{'Code_datalist':Code_datalist})
