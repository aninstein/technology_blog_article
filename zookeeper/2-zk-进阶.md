# 学习zookeeper的教程-进阶

## 1. 四字命令

zookeeper 支持某些特定的四字命令与其交互，用户获取 zookeeper 服务的当前状态及相关信息，用户在客户端可以通过 telenet 或者 nc（netcat） 向 zookeeper 提交相应的命令。

```
# 安装 nc 命令：
yum install nc                # centos
```

四字命令格式：
```
echo [command] | nc [ip] [port]
```

最简单的，比如查看zk节点状态：
```
[root@localhost ~]# echo stat | nc 172.17.0.2 2181
Zookeeper version: 3.7.0-e3704b390a6697bfdf4b0bef79e3da7a4f6bac4b, built on 2021-03-17 09:46 UTC
Clients:
 /172.17.0.1:42690[0](queued=0,recved=1,sent=0)

Latency min/avg/max: 0/0.6499/48
Received: 438
Sent: 437
Connections: 1
Outstanding: 0
Zxid: 0x300000004
Mode: follower
Node count: 8
```

ZooKeeper 常用四字命令主要如下：

- **conf**：	3.3.0版本引入的。打印出服务相关配置的详细信息。
- **cons**：	3.3.0版本引入的。列出所有连接到这台服务器的客户端全部连接/会话详细信息。包括"接受/发送"的包数量、会话id、操作延迟、最后的操作执行等等信息。
- **crst**：	3.3.0版本引入的。重置所有连接的连接和会话统计信息。
- **dump**：	列出那些比较重要的会话和临时节点。这个命令只能在leader节点上有用。
- **envi**：	打印出服务环境的详细信息。
- **reqs**：	列出未经处理的请求
- **ruok**：	测试服务是否处于正确状态。如果确实如此，那么服务返回"imok"，否则不做任何相应。
- **stat**：	输出关于性能和连接的客户端的列表。
- **srst**：	重置服务器的统计。
- **srvr**：	3.3.0版本引入的。列出连接服务器的详细信息
- **wchs**：	3.3.0版本引入的。列出服务器watch的详细信息。
- **wchc**：	3.3.0版本引入的。通过session列出服务器watch的详细信息，它的输出是一个与watch相关的会话的列表。
- **wchp**：	3.3.0版本引入的。通过路径列出服务器watch的详细信息。它输出一个与session相关的路径。
- **mntr**：	3.4.0版本引入的。输出可用于检测集群健康状态的变量列表

参考官方链接：https://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_4lw