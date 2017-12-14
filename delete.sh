#!/bin/bash
docker stop dabaredis
docker stop dabamysql
docker stop dabadjango
docker stop dabanginx-server
docker rm -v dabaredis
docker rm -v dabamysql
docker rm -v dabadjango
docker rm -v dabanginx-server
docker rmi daba0007/dabanginx
docker rmi daba0007/django-app 
