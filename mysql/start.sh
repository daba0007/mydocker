#!/bin/bash 
    #
echo "---------------start mysql image-------------------"
docker run --name dabamysql \
-v $(pwd)/conf.d:/etc/mysql/conf.d \
-v $(pwd)/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=root \
-p 3307:3306 \
-d daba0007/mysql
