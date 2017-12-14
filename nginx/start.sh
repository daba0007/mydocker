#!/bin/bash 
#                                                                                                                   
docker build -t daba0007/dabanginx .        
docker run --name dabanginx-server \
--link  dabadjango:web  \
-v /www/static \
--volumes-from dabadjango \
-p 8888:80 \
-d daba0007/dabanginx
