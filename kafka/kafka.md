# Kafka学习手册
---
---

## 0. 预备动作
- 安装java
```
yum install java java-devel
```
下载软件包：
```
wget https://www.apache.org/dyn/closer.cgi?path=/kafka/2.7.0/kafka_2.13-2.7.0.tgz
```
解压即可，kafka依赖zookeeper进行管理。而在下载的kafka执行文件当中已经包括了zookeeper，并不需要单独安装zookeeper。

## 1. zookeeper
### 1.1 启动zookeeper
kafka本身安装包中自带了zookeeper的启动软件，kafka的集群模式依赖于zookeeper，因此需要先启动zookeeper才能启动kafka

### 1.2 使用本地的zookeeper
kafka可以使用本地的zookeeper


## 2. 安装kafka
先启动zookeeper服务器：
```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

然后启动kafka：
```
bin/kafka-server-start.sh config/server.properties
```

使用ps查看服务已经起来了：
```

```