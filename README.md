### web搭建
登录docker hub，申请一个仓库


本次试验环境：阿里云服务器 Centos7.2 x86_64

所需知识：python,redis,mysql,django,nginx，linux操作知识

逻辑图：
```
                                -> mysql
web -> nginx -> uwsgi ->django       |
                                -> redis
```
### 预备工作
安装docker
```bash
# vim /etc/yum.repos.d/docker.repo
[dockerrepo]

name=Docker Repository

baseurl=https://yum.dockerproject.org/repo/main/centos/7/

enabled=1

gpgcheck=1

gpgkey=https://yum.dockerproject.org/gpg

 

# yum install docker-engine -y

systemctl restart docker
```
docker安装成功之后，使用docker下载所需镜像(由于一些镜像下载速度过慢，我搭建了自己的镜像仓库，拉去会快一点)
* daba0007/nginx
* daba0007/redis
* daba0007/python2.7(如果环境有需要可以使用daba0007/python3.6)
* daba0007/mysql
* daba0007/django

拉取完之后确定试验的目录
```bash
# mkdir /daba0007
# cd /daba0007/
# mkdir mysql redis nginx web
```

### 配置

1. 创建mysql容器

创建容器之前要把原先的数据库放置到mysql文件夹中,这一步需要把原先的数据从原来的数据库中导出来，我使用的是mysql,之前数据在form数据库中，操作如下：
```bash
# cd mysql
# mkdir conf.d
# cd conf.d
# mysqldump -u root -p --database form > form.sql
# cd ..
# cat mysql.sh
#!/bin/bash

docker run --name dabamysql \
-v $(pwd)/conf.d:/etc/mysql/conf.d \
-v $(pwd)/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
-p 3307:3306 \
-d daba0007/mysql

```
之后会创建一个名为dabamysql的容器，其中
* -v指定容器的配置文件目录与数据目录
* -e设置环境变量，在上述脚本中为初始化数据库密码
* -p指定端口,主机端口:容器内端口
* -d创建一个守护态的容器，不会因为退出而结束

完成这一步之后需要将数据库的数据导入dabamysql容器中
```
# docker inspect --format "{{.State.Pid}}" dabamysql
8971
# nsenter --target 8971 --mount --uts --ipc --net --pid
root@3d85f4c9f4f8:/# cd /etc/mysql/conf.d/
root@3d85f4c9f4f8:/etc/mysql/conf.d# mysql -uroot -p form < form.sql
```

2. 创建redis容器
```bash
# cd redis
# cat redis.sh
#!/bin/bash

docker run --name dabaredis -d daba0007/redis
```
之后会创建一个名为dabaredis的容器

3. 创建 django 容器

首先基于daba0007/python2.7的镜像使用dockerfile来安装 django 所需的环境并生成一个新的镜像，需要一个编写完成的django项目(不要纠结我的django，我就花了两个钟头随便写了一个能够实现连接mysql实现查询的django，难看就难看吧T^T)，可以使用tar进行压缩比如我的mysql目录
```bash
# cd mysql
# ls
dabaweb.tar.gz dockerfile start.sh 
```
dockerfile在生成新的镜像时会解压这个tar包，所以不用担心解压问题。需要关心的是这个requirements.txt文件，在之前编写django的时候会有许多通过pip安装的服务，写入requirement中，然后在脚本执行时会在新容器中安装，编写dockerfile文件
```bash
FROM daba0007/python2.7

MAINTAINER daba0007

ADD dabaweb.tar.gz /usr/src/

WORKDIR /usr/src/dabaweb

RUN pip install --no-cache-dir -r requirement.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

```
然后编写执行脚本
```bash
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

```
其中：
* -link能够进行容器间的通信，容器名：别名，然后启动一个uwsgi来启动django程序。
* django中setting的参数需要注意，因为我使用的mysql是通过容器端口来连接的，连接的数据库是mysql,所以host也是写的mysql(因为这个500的问题搞了我一个晚上T^T)
    ```bash
    DATABASES = {
    
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'form',
            'USER':'root',
            'PASSWORD':'123456',
            #'HOST':'127.0.0.1'
            'HOST':'mysql',
            'PORT':'3306',
        }
    
    }

    ```
* 之后就可以通过访问网址http://你的ip:12000看到网站，不过这时候的网站是没有加载样式的，还需要nginx来帮忙处理静态文件

4. 创建 nginx 容器

nginx容器首先要配置好conf文件，放置在nginx-conf中
```bash
cd nginx
mkdir nginx-conf
cat django_project.conf
server {

    listen 80;
    server_name localhost;
    charset utf-8;
    root   /usr/src/dabaweb;
    access_log  /var/log/nginx/django.log;

    location ^~ /static {
        alias /usr/src/dabaweb/static;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

}

```
然后编写dockerfile文件，使用daba0007/nginx创建一个nginx配置完毕的容器
```bash
FROM daba0007/nginx

MAINTAINER daba0007

RUN rm /etc/nginx/conf.d/default.conf
ADD nginx-conf/ /etc/nginx/conf.d/

```
然后再编写脚本
```bash
#!/bin/bash

docker build -t daba0007/dabanginx .
docker run --name dabanginx-server \
--link  dabadjango:web  \
-v /www/static \
--volumes-from dabadjango \
-p 8888:80 \
-d daba0007/dabanginx

```
至此，所有的容器都创建完毕,之后通过访问http://你的ip:8888/就可以看到网址了（前提是你的django的url不要写错）
