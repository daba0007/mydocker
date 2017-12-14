#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from form.models import User,User_data,Code_data

def home(request):
    return render(request, 'home.html')

def user_data(request):
    User_datalist = User_data.objects.all()
    return render(request, 'user_data.html',{'User_datalist':User_datalist})

def code_data(request):
    Code_datalist = Code_data.objects.all()
    return render(request, 'code_data.html',{'Code_datalist':Code_datalist})
