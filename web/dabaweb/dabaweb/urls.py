# -*- coding:utf-8 -*-
from django.conf.urls import url,include
from django.contrib import admin
from form import views as form_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',form_views.home, name='home'),
    url(r'^User_data$',form_views.user_data, name='user_data'),
    url(r'^Code_data$',form_views.code_data, name='code_data'),
]
