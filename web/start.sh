#!/bin/bash 
# 
docker exec -d dabamysql mysql -uroot -p123456 -e "create database form;"
docker build -t daba0007/django-app .
docker run --name dabadjango \
-v /usr/src/dabaweb \
-v /usr/src/dabaweb/static \
--link dabamysql:mysql \
--link dabaredis:redis \
-p 12000:8000 \
-d daba0007/django-app  /usr/local/bin/uwsgi --http :8000 --chdir /usr/src/dabaweb -w dabaweb.wsgi
