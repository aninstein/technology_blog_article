# 学习zookeeper的教程
## 1. 安装zookeeper
### 1.1 先安装zookeeper，[参考链接https://www.cnblogs.com/jimcsharp/p/8358271.html](https://www.cnblogs.com/jimcsharp/p/8358271.html)

下载zookeeper
```
mkdir zookeeper
cd zookeeper
wget https://www.apache.org/dyn/closer.lua/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2-bin.tar.gz
tar xvf apache-zookeeper-3.6.2-bin.tar.gz
```


- bin目录
  zk的可执行脚本目录，包括zk服务进程，zk客户端，等脚本。其中，.sh是Linux环境下的脚本，.cmd是Windows环境下的脚本。
- conf目录
  配置文件目录。zoo_sample.cfg为样例配置文件，需要修改为自己的名称，一般为zoo.cfg。log4j.properties为日志配置文件。
- lib
- zk依赖的包。
- contrib目录
  一些用于操作zk的工具包。
  recipes目录
  zk某些用法的代码示例


修改配置文件：
把zoo_sample.cfg建立一个备份，命名为zoo.cfg

- tickTime
    - 时长单位为毫秒，为zk使用的基本时间度量单位。例如，1 * tickTime是客户端与zk服务端的心跳时间，2 * tickTime是客户端会话的超时时间。
    - tickTime的默认值为2000毫秒，更低的tickTime值可以更快地发现超时问题，但也会导致更高的网络流量（心跳消息）和更高的CPU使用率（会话的跟踪处理）。
- clientPort
    - zk服务进程监听的TCP端口，默认情况下，服务端会监听2181端口。
- dataDir
    - 无默认配置，必须配置，用于配置存储快照文件的目录。如果没有配置dataLogDir，那么事务日志也会存储在此目录。


### 1.2 启动zookeeper

在Linux环境下，进入bin目录，执行命令
```
./zkServer.sh start ../conf/zoo.cfg
```
这个命令使得zk服务进程在后台进行。如果想在前台中运行以便查看服务器进程的输出日志，可以通过以下命令运行：
```
./zkServer.sh start-foreground
```
执行此命令，可以看到大量详细信息的输出，以便允许查看服务器发生了什么。

使用vim打开zkServer.sh文件，可以看到其会zkEnv.sh脚本。zkEnv脚本的作用是设置zk运行的一些环境变量，例如配置文件的位置和名称等。

### 1.3 使用systemctl管理zookeeper
当然也可以把zookeeper使用systemctl接管。
在/usr/lib/systemd/system下创建文件zookeeper.service，编辑文件内容：
```ini
[Unit]
Description=Zookeeper Service unit Configuration
After=network.target

[Service]
Type=forking
PIDFile=/tmp/zookeeper/zookeeper_server.pid
Environment=JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.275.b01-1.el8_3.x86_64/bin
ExecStart=/opt/zookeeper/bin/zkServer.sh start /opt/zookeeper/conf/zoo.cfg
ExecStop=/opt/zookeeper/bin/zkServer.sh stop
ExecStartPre=/usr/bin/rm -f /tmp/zookeeper/zookeeper_server.pid
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=none
User=root
Group=root
Restart=on-failure
[Install]
WantedBy=multi-user.target
```
其中的：
- PIDFile：为zoo.cfg中定义的dataDir目录下的zookeeper_server.pid
- Environment：需要依赖java环境
- ExecStart：启动脚本
- ExecStop：关闭脚本
- ExecStartPre：启动前准备


保存文件后，执行：
```
systemctl daemon-reload  # 更新unit文件
systemctl enable zookeeper  # 开机启动（如果有需要的话）
systemctl start zookeeper  # 启动程序
```

### 1.3 连接zookeeper
zk分为server和client，它们的作用是：
- server：服务端运行在集群的每台机器当中，在急群众提供服务。 
- client：客户端是集群外的访问，服务端才是集群上的提供服务的。  


使用bin/zkServer.sh start开启的zookeeper上的一个服务端，而使用bin/zkCli.sh是将客户端连到服务端上。

客户端可以通过服务端创建znode,删除znode，写znode,读znode，设置监视等等。

其中zookeeper提供的master选举选的是客户端的master，根据他们登录后在GroupMember目录下创建的临时目录的id来选的，最小的是master。  

这就区别于集群中服务端的各个servers的角色了，servers角色是leader和follow（或者还有observer）。 简而言之，客户端通过服务端来获取到zookeeper提供的服务。



## 2. 理论知识和名词描述
### 2.1 