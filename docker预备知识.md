### docker安装

1. 设置yum源并安装docker
```
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
2. 下载最新的docker镜像
```
docker pull ubuntu
```
如果要下载指定版本的镜像，可以使用
```
docker pull ubuntu:14.04
```
以上两条命令都相当于
```
docker pull registry.hub.docker.com/ubuntu:latest
```
这是从默认的注册服务器registry.hub.docker.com中ubuntu仓库来下载,也可以指定其他docker源

下载到本地之后，就可以使用该镜像了，例如使用镜像创建一个容器，在其中运行bash应用
```
docker run -t  -i ubuntu /bin/bash
```

3. 查看镜像信息
 
使用docker image可以列出本地主机上已有的镜像,表明了信息：
* 仓库
* 标签信息
* 镜像id号
* 创建时间
* 镜像大小
```
# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              20c44cd7596f        2 weeks ago         123MB

```
可以使用docker tag命令为本地添加一个新的标签，指向同一个镜像文件，只是别名不同而已。

可以使用docker inspect命令获取该镜像的详细信息
```
[root@python docker]# docker inspect 20c44cd7596f
[
    {
        "Id": "sha256:20c44cd7596ff4807aef84273c99588d22749e2a7e15a7545ac96347baa65eda",
        "RepoTags": [
            "ubuntu:latest"
        ],
        "RepoDigests": [
            "ubuntu@sha256:7c67a2206d3c04703e5c23518707bdd4916c057562dd51c74b99b2ba26af0f79"
        ],
        "Parent": "",
        "Comment": "",
        "Created": "2017-11-17T21:59:25.014645802Z",
        "Container": "e5f1a9df75b86a5d803eaf6f3fed6a0f8ef5fbf15a6c5039df087e4348ed8171",
        "ContainerConfig": {
            "Hostname": "e5f1a9df75b8",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "/bin/sh",
                "-c",
                "#(nop) ",
                "CMD [\"/bin/bash\"]"
            ],
            "ArgsEscaped": true,
            "Image": "sha256:b5771e7d8dcc594b886dbdd6a9c3de60d45252ca657dfdff6e1d996728dfa2cd",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": {}
        },
        "DockerVersion": "17.06.2-ce",
        "Author": "",
        "Config": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "/bin/bash"
            ],
            "ArgsEscaped": true,
            "Image": "sha256:b5771e7d8dcc594b886dbdd6a9c3de60d45252ca657dfdff6e1d996728dfa2cd",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": null
        },
        "Architecture": "amd64",
        "Os": "linux",
        "Size": 122783944,
        "VirtualSize": 122783944,
        "GraphDriver": {
            "Data": {
                "RootDir": "/var/lib/docker/overlay/40292116a4e2e5acd3382578224bb9b0a8264dadbbb79445902ac516002c912e/root"
            },
            "Name": "overlay"
        },
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:788ce2310e2fdbbf81fe21cbcc8a44da4cf648b0339b09c221abacb4cd5fd136",
                "sha256:aa4e47c4511638484cd5d95eadd7a8e4da307375ba31ff50d47aa9065dce01e0",
                "sha256:b3968bc26fbd527f214f895aeef940a6930c62d853fe8b12bd479f0b53518150",
                "sha256:c9748fbf541d3e043521e165b015d45825de33c00a8acb037443cfbd0cb5e677",
                "sha256:2f5b0990636a87f1557d64ba39808dcd64031328b2a159c5805115b8e725bbbc"
            ]
        }
    }
]

```
docker inspect 命令返回的是一个JSON格式的信息，如果我们只要其中一项内容，可以使用-f参数来指定
```
docker inspect -f {{".Id"}}  20c
sha256:20c44cd7596ff4807aef84273c99588d22749e2a7e15a7545ac96347baa65eda
```
在指定镜像ID的时候，通常使用该id的前若干个字符组成的可区分子串来替代完整的ID

4. 搜寻镜像
使用docker search命令可以搜索远程仓库中共享的镜像，默认搜索官方docker Hub官方仓库中的镜像，用法为docker search TERM，支持的参数包括：
* --automated=false仅显示自动创建的镜像
* --no-trunc=false输出信息不截断显示
* -s, --stars=0指定仅显示评价为指定星级以上的镜像

例如，搜索带mysql关键字的镜像如下所示：
```
[root@python docker]# docker search mysql
NAME                                                   DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
mysql                                                  MySQL is a widely used, open-source relati...   5327      [OK]       
mariadb                                                MariaDB is a community-developed fork of M...   1657      [OK]       
mysql/mysql-server                                     Optimized MySQL Server Docker images. Crea...   370                  [OK]
percona                                                Percona Server is a fork of the MySQL rela...   305       [OK]       
hypriot/rpi-mysql                                      RPi-compatible Docker Image with Mysql          74                   
zabbix/zabbix-server-mysql                             Zabbix Server with MySQL database support       65                   [OK]
centurylink/mysql                                      Image containing mysql. Optimized to be li...   54                   [OK]
sameersbn/mysql                                                                                        48                   [OK]
zabbix/zabbix-web-nginx-mysql                          Zabbix frontend based on Nginx web-server ...   39                   [OK]
tutum/mysql                                            Base docker image to run a MySQL database ...   29                   
1and1internet/ubuntu-16-nginx-php-phpmyadmin-mysql-5   ubuntu-16-nginx-php-phpmyadmin-mysql-5          19                   [OK]
schickling/mysql-backup-s3                             Backup MySQL to S3 (supports periodic back...   16                   [OK]
centos/mysql-57-centos7                                MySQL 5.7 SQL database server                   15                   
linuxserver/mysql                                      A Mysql container, brought to you by Linux...   13                   
mysql/mysql-cluster                                    Experimental MySQL Cluster Docker images. ...   11                   
centos/mysql-56-centos7                                MySQL 5.6 SQL database server                   6                    
openshift/mysql-55-centos7                             DEPRECATED: A Centos7 based MySQL v5.5 ima...   6                    
frodenas/mysql                                         A Docker Image for MySQL                        3                    [OK]
dsteinkopf/backup-all-mysql                            backup all DBs in a mysql server                3                    [OK]
circleci/mysql                                         MySQL is a widely used, open-source relati...   2                    
cloudfoundry/cf-mysql-ci                               Image used in CI of cf-mysql-release            0                    
ansibleplaybookbundle/rhscl-mysql-apb                  An APB which deploys RHSCL MySQL                0                    [OK]
astronomerio/mysql-sink                                MySQL sink                                      0                    [OK]
inferlink/landmark-mysql                               landmark-mysql                                  0                    [OK]
cloudposse/mysql                                       Improved `mysql` service with support for ...   0                    [OK]
```
5. 删除镜像

使用镜像的标签删除镜像，使用docker rmi命令可以删除镜像，命令格式为docker rmi IMAGE[IMAGE...],其中IMAGE可以为标签或ID
```
docker rmi ubuntu
```
如果有多个标签指向同一个镜像是，命令只是删除指定标签。但镜像只剩下一个标签再使用docker rmi就会彻底删除该镜像

当有该镜像创建的容器存在时，镜像文件默认是无法被删除的。

6. 创建镜像
* 基于已有镜像的容器创建
    
    该方法主要使用docker commit命令。命令格式为docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]],主要选项包括：
    * -a, --author="" 作者信息
    * -m, --message=""提交信息
    * -p， --pause=true提交时暂停容器运行
    ```
    docker run -ti ubuntu /bin/bash                                     # 使用容器创建一个test
    docker commit -m "Added a new file" -a "wangshuo" 0e68148992dc test # 使用ID或名称来指定容器创建新的镜像
    ```
* 基于本地模板导入

    可以直接从一个操作系统模板文件导入一个镜像。(OpenVZ模板)
* 基于dockerfile创建

7. 存入和载入镜像
    
可以使用docker save和docker load命令来存出和载入镜像

* 存出镜像

存出镜像到本地文件
```
docker images
docker save -o ubuntu.tar ubuntu
```
* 载入镜像

可以使用docker load从存出的本地文件中再导入到本地镜像库
```
docker load --input ubuntu.tar
```
或
```
docker load < ubuntu.tar
```
这将导入镜像以及其相关的元数据信息（包括标签），可以使用docker images命令进行查看

8. 上传镜像

在dockerHUB网站注册后就可以上传自制的镜像

### 容器

docker容器是独立运行的一个或一组应用，以及它们的必需运行环境

1. 创建容器
```
docker create -it ubuntu
```
使用docker create命令新建的容器处于停止状态，可以使用docker start命令来启动它

* 新建并启动容器
    ```
    docker run  ubuntu /bin/echo 'Hello world'
    ```
    利用docker run来创建并启动容器的时候，docker在后台运行的标准操作包括：
    * 检查本地是否存在指定的镜像，不存在就从公有仓库下载
    * 利用镜像创建并启动一个容器
    * 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
    * 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
    * 从地址池配置一个IP地址给容器
    * 执行用户指定的应用程序
    * 执行完毕后容器被终止
    
    -t 让docker分配一个伪终端(pseudo-tty)并绑定到容器的标准输入上
    
    -i 让容器的标准输入保持打开
    
* 守护态运行

    让docker容器在后台以守护态形式运行。用户通过添加-d参数来实现。
    ```
    docker run -d ubuntu /bin/sh -c "while true; do echo hello world;sleep 1;done"
    ```
    容器启动后会返回一个唯一的id，也可以通过docker ps命令来查看容器信息
    
    可以使用docker logs 来查看输出信息
    
2. 终止容器
    
可以使用docker stop来停止一个正在运行中的容器

可以使用docker ps -a -q命令看到处于终止状态的容器的ID信息

处于终止状态的容器，可以通过docker start/restart命令来重新启动

3. 进入容器

在使用-d参数时，容器启动后会进入后台，用户无法看到容器中的信息。某些时候需要进入容器进行操作

* attach
    ```
    docker sttach
    ```
    但使用attach命令并不方便，当多个窗口同时attach到同一个容器的时候，所有窗口都会同步显示。当某个窗口因命令阻塞时，其他窗口也无法执行操作了。

* exec
    ```
    docker exec -ti ····· /bin/bash
    ```
* nsenter

    nsenter工具在util-linux包2.23版本后包含
    
    通过$(docker-pid ····)可以得到容器pid
    
    执行
    ```
    docker --target $PID --mount --uts --ipc --net --pid
    ```

4. 删除容器

使用docker rm删除处于终止状态的容器
* -f, --force=false 强行终止并删除一个运行中的容器
* -l, --link=false 删除容器的连接，但保留容器
* -v，--volumes=false 删除容器挂载的数据卷

5. 导入和导出容器

* 导出容器

导出容器是指导出一个已经创建的容器到一个文件，不管此时容器是否处于运行状态，可以使用docker export命令。

```
docker export ce5 > test_for_run.tar
```
可将这些文件传输到其他机器上，在其他机器上通过导入实现容器的迁移

* 导入容器

导出的容器可以使用docker import命令导入，成为镜像
```
cat test_for_run.tar |sudo docker import - test/ubuntu:v1.0
```
既可以使用docker load命令导入镜像文件，又可以使用docker import命令来导入一个容器快照到本地镜像库。这两者的区别在于容器快照文件将丢弃所有的历史记录和元数据信息（仅保存容器当时的快照状态），镜像存储文件将保存完整记录。此外，从容器快照文件导入时可以重新指定标签等元数据信息

### 仓库
1. 创建和使用私有仓库

可以使用官方提供的registry镜像来简单的搭建一套本地私有仓库环境：
```
docker run -d -p 5000:5000 registry
```
这将自动下载并启动一个registry容器，创建本地的私有仓库服务

默认情况下，会将仓库创建在容器的/tmp/registry目录下。可以通过-v参数来将镜像文件存放在本地的指定路径上
```
docker run -d -p 5000:5000 -v /opt/data/registry:/tmp/registry registry
```
此时，在本地将启动一个私有仓库服务，监听端口为5000

2. 管理私有仓库镜像

```
docker push $path/ubuntu
```

### 数据管理
1. 数据卷

数据卷是一个可供容器使用的特殊目录
* 数据卷可以在容器之间共享和重用
* 对数据卷的修改会立马生效
* 对数据卷的更新，不会影响镜像
* 卷会一直存在，直到没有容器使用

使用-v标记可以在容器内创建一个数据卷，多次使用-v标记可以创建多个数据卷

```
docker run -d -P --name web -v /webapp training /webapp python app.py                   # 使用training/webapp镜像创建一个WEB容器，并创建一个数据卷挂载到容器的/webapp目录
```

挂载一个主机目录作为数据卷
```bash
docker run -d -P --name web -v /src/webapp:/opt/webapp trainging/webapp python app.py   # 加载主机的/src/webapp目录到容器的/opt/webapp目录
```
本地目录的路径必须是绝对路径，如果路径不存在，docker会自动创建

docker挂载数据卷的默认权限是读写（rw）,用户也可以通过ro指定为只读
```
docker run -d -P --name web -v /src/webapp:/web/webapp:ro training/webapp python app.py
```
增加了:ro之后，容器内挂载的数据卷的数据就无法修改了

挂载一个本地主机文件作为数据卷
```
docker run --rm --it -v ~/.bash_history:/.bash_history ubuntu /bin/bash 
```
这样就可以记录在容器输入过的命令历史了

>如果直接挂载一个文件到容器，使用文件编辑工具，可能会造成文件inode的改变，从docker1.1.0起，这会导致报错误信息。所以推荐的方式是直接挂载文件所在的目录

2. 数据卷容器

如果用户需要在容器之间共享一些持续更新的数据，最简单的方式是使用数据卷容器。

首先，创建一个数据卷容器dbdata，并在其中创建一个数据卷挂载到/dbdata:
```
docker run -it -v /dbdata --name dbdata ubuntu
```
然后，可以使用其他容器中使用的--volumes-from 来挂载dbdata容器中的数据卷
```
docker run -it --volumes-from dbdata --name db1 ubuntu
docker run -it --volumes-from dbdata --name db2 ubuntu
```
此时，容器db1和db2都挂载同一个数据卷到相同的/dbdata目录。三个容器任何一方在该目录下的写入，其他容器都可以看到

可以多次使用--volumes-from参数来从多个容器挂载多个数据卷，还可以从其他已经挂载了的容器卷的容器来挂载数据卷
```
docker run -d --name db3 --volumes-from db1 trainging/postgres
```
>使用--volumes-from参数所挂载数据卷的容器自身并不需要保持在运行状态

如果删除了挂载的容器，数据卷并不会自动删除。如果要删除一个数据卷，必须删除最后一个还挂载这它的容器时显式使用
```
docker rm -v
```
来指定同时删除关联的容器

3. 使用数据卷容器迁移数据

备份
```
docker run --volumes-from dbdata -v $(pwd):/backup --name worker ubuntu tar cvf /backup/backup.tar /dbdata
```
恢复
```
docker run -v /dbdata --name dbdata2 ubuntu /bin/bash
```
然后创建另一个新的容器，挂载dbdata2的容器，并使用untar解压备份文件到所挂载的容器卷中即可
```
docker run --volumes-from dbdata2 -v $(pwd):/backup busybox tar xvf /backup/backup.tar
```

### 网络基础管理
1. 端口映射实现访问容器

在启动容器的时候，如果不指定对应参数，在容器外部是无法通过网络来访问容器内的网络应用和服务的。

当容器中运行一些网络应用，要让外部访问这些应用时，可以通过-P或-p参数来指定端口映射。

当使用-P标记时，Docker会随机映射一个49000~49900的端口至容器内部开放的网络端口

当使用-p则可以指定要映射的端口，并且在一个指定端口上只可以绑定一个容器

* 映射所有接口地址
    
    使用
    ```
    docker run -d -p 5000:5000 training/webapp python app.py    # 将本地的5000端口映射到容器的5000端口，本地:容器
    ```
    此时默认会绑定本地所有接口上的所有地址。多次使用-p可以绑定多个端口
    ```
    docker run -d -p 5000:5000 -p 3000:80 training/webapp python app.py
    ```

* 映射到指定地址的指定端口
    ```
    docker run -d -p 127.0.0.1:5000:5000 training/webapp python app.py
    ```
* 映射到指定地址的任意端口
    
    本地主机会自动分配一个端口
    ```
    docker run -d -p 127.0.0.1::5000 training/webapp python app.py
    ```
    还可以使用udp标记来指定udp端口
    ```
    docker run -d -p 127.0.0.1:5000:5000/udp training/webapp python app.py
    ```
    查看映射端口配置
    ```
    docker port nostalgic_morse 5000
    ```
    
2. 容器互联实现容器间通信


容器的连接除了端口映射外另一种可以与容器中应用进行交互的方式，它会在源和接受容器之间
* 自定义容器命名

连接系统依据容器的名称来执行。当创建容器的时候，系统会默认分配一个名字。

可以使用--name web training/webapp python app.py
```
docker run -d -p --name web training/webapp python app.py
```
在执行docker run 的时候如果添加-- rm 标记，则容器在终止后会立刻删除。
>--rm和-d参数不能同时使用

* 容器互联

    使用--link参数可以让容器之间安全的进行交互
    ```
    docker run -d --name db training/postgres
    ```
    删除之前创建的web容器
    ```
    docker rm -f web
    ```
    然后创建一个新的web容器，并将它连接到db容器
    ```
    docker run -d -P --name web --link db:db training training/webapp python app.py 
    ```
    此时，db容器和web容器建立互联关系,--link name:alias,name是要连接的容器的名字，alias是这个连接的别名
    
    docker在两个互联的容器之间创建了一个安全隧道，而且不用映射它们的端口到宿主主机上。在启动db容器的时候没有使用-p或-P标记，从而避免了暴露数据库端口到外部网络上。
    
    Docker通过两种方式为容器公开连接信息
    * 环境变量
    * 更新/etc/hosts文件
    使用env命令来查看web容器的环境变量：
    ```
    docker run -rm --name web2 --link db:db training/webapp env
    ```
    其中DB_开头的环境变量是供web容器连接db容器使用，前缀使用大写的连接别命名
    
    除了环境变量，Docker还添加host信息到父容器的/etc/hosts的文件。
    ```
    docker run -t -i --rm --link db:db training/webapp /bin/bash
    root@20c44cd7596f:/opt/webapp# cat /etc/hosts
    172.17.0.7 20c44cd7596f
    ···
    172.17.0.5 db
    ```
    这里有两个hosts，第一个是web容器，web容器用自己的id作为默认主机名，第二个是db容器的ip和主机名，可以在web容器中安装ping命令来测试跟db容器的连通。
    

### Kubernetes

Kubernetes是一个开源平台，用于跨主机群集自动部署，扩展和操作应用程序容器，提供以容器为中心的基础架构。

使用Kubernetes，您可以快速高效地响应客户需求：
* 快速，可预测地部署应用程序。
* 在运行中扩展应用程序。
* 无缝推出新功能。
* 仅使用您需要的资源来优化硬件的使用。

我们的目标是建立一个组件和工具的生态系统，以减轻在公共云和私有云中运行应用程序的负担。

主要功能如下：
* 将多台Docker主机抽象为一个资源，以集群方式管理容器，包括任务调度、资源管理、弹性伸缩、滚动升级等功能。
* 使用编排系统（YAML File）快速构建容器集群，提供负载均衡，解决容器直接关联及通信问题
* 自动管理和修复容器，简单说，比如创建一个集群，里面有十个容器，如果某个容器异常关闭，那么，会尝试重启或重新分配容器，始终保证会有十个容器在运行，反而杀死多余的。

kubernetes角色组成：
* Pod
    
    Pod是kubernetes的最小操作单元，一个Pod可以由一个或多个容器组成；
    
    同一个Pod只能运行在同一个主机上，共享相同的volumes、network、namespace；

* ReplicationController（RC）

    RC用来管理Pod，一个RC可以由一个或多个Pod组成，在RC被创建后，系统会根据定义好的副本数来创建Pod数量。在运行过程中，如果Pod数量小于定义的，就会重启停止的或重新分配Pod，反之则杀死多余的。当然，也可以动态伸缩运行的Pods规模。
    
    RC通过label关联对应的Pods，在滚动升级中，RC采用一个一个替换要更新的整个Pods中的Pod。

* Service

    Service定义了一个Pod逻辑集合的抽象资源，Pod集合中的容器提供相同的功能。集合根据定义的Label和selector完成，当创建一个Service后，会分配一个Cluster IP，这个IP与定义的端口提供这个集合一个统一的访问接口，并且实现负载均衡。

* Label

    Label是用于区分Pod、Service、RC的key/value键值对； 
    
    Pod、Service、RC可以有多个label，但是每个label的key只能对应一个；
    
    主要是将Service的请求通过lable转发给后端提供服务的Pod集合；

kubernetes组件组成：
* kubectl

    客户端命令行工具，将接受的命令格式化后发送给kube-apiserver，作为整个系统的操作入口。

* kube-apiserver

    作为整个系统的控制入口，以REST API服务提供接口。

* kube-controller-manager

    用来执行整个系统中的后台任务，包括节点状态状况、Pod个数、Pods和Service的关联等。

* kube-scheduler

    负责节点资源管理，接受来自kube-apiserver创建Pods任务，并分配到某个节点。

* etcd

    负责节点间的服务发现和配置共享。

* kube-proxy

    运行在每个计算节点上，负责Pod网络代理。定时从etcd获取到service信息来做相应的策略。

* kubelet

    运行在每个计算节点上，作为agent，接受分配该节点的Pods任务及管理容器，周期性获取容器状态，反馈给kube-apiserver。

* DNS

    一个可选的DNS服务，用于为每个Service对象创建DNS记录，这样所有的Pod就可以通过DNS访问服务了。
    
```
基本部署步骤：

1）minion节点安装docker

2）minion节点配置跨主机容器通信

3）master节点部署etcd、kube-apiserver、kube-controller-manager和kube-scheduler组件

4）minion节点部署kubelet、kube-proxy组件
```
