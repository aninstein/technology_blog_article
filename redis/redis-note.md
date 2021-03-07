# Redis学习笔记
---
---
## 1. redis安装
### 1.1 简介
 Redis 是完全开源的，遵守 BSD 协议，是一个高性能的 key-value 数据库。

Redis 与其他 key - value 缓存产品有以下三个特点：

- Redis支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。
- Redis不仅仅支持简单的key-value类型的数据，同时还提供list，set，zset，hash等数据结构的存储。
- Redis支持数据的备份，即master-slave模式的数据备份。 

### 1.2 源码安装
Linux 源码安装

下载地址：http://redis.io/download，下载最新稳定版本。

本教程使用的最新文档版本为 2.8.17，下载并安装：
```
# wget http://download.redis.io/releases/redis-6.0.8.tar.gz
# tar xzf redis-6.0.8.tar.gz
# cd redis-6.0.8
# make
```
执行完 make 命令后，redis-6.0.8 的 src 目录下会出现编译后的 redis 服务程序 redis-server，还有用于测试的客户端程序 redis-cli：

下面启动 redis 服务：
```
# cd src
# ./redis-server
```
注意这种方式启动 redis 使用的是默认配置。也可以通过启动参数告诉 redis 使用指定配置文件使用下面命令启动。
```
# cd src
# ./redis-server ../redis.conf
```
redis.conf 是一个默认的配置文件。我们可以根据需要使用自己的配置文件。

启动 redis 服务进程后，就可以使用测试客户端程序 redis-cli 和 redis 服务交互了。 比如：
```shell
# cd src
# ./redis-cli
redis> set foo bar
OK
redis> get foo
"bar"
```
### 1.3 yum安装
```
yum install redis -y
```

### 1.4 配置redis和启动
redis分为server和client端，我们一般都只是启用redis的server端，在上面说的可以通过./redis-server来启动redis，如果是yum安装的话，可以通过systemctl来管理redis
```
# cd src
# ./redis-server ../redis.conf

systemctl status/start/stop/restart/reload redis
```

可以看到，redis的配置是在redis.conf配置文件当中的。
具体的redis的配置可以看：https://www.runoob.com/redis/redis-conf.html

常用的配置项包括：
|参数|作用|
|-|-|
loglevel notice |指定日志记录级别，Redis 总共支持四个级别：debug、verbose、notice、warning，默认为 notice
timeout 300|当客户端闲置多长秒后关闭连接，如果指定为 0 ，表示关闭该功能 
bind 127.0.0.1|绑定的主机地址 
logfile stdout|日志记录方式，默认为标准输出，如果配置 Redis 为守护进程方式运行，而这里又配置为日志记录方式为标准输出，则日志将会发送给 /dev/null 
databases 16|设置数据库的数量，默认数据库为0，可以使用SELECT 命令在连接上指定数据库id 
save <seconds\> <changes\>|指定在多长时间内，有多少次更新操作，就将数据同步到数据文件，可以多个条件配合<br>Redis 默认配置文件中提供了三个条件：<br>save 900 1<br>save 300 10<br>save 60 10000<br>分别表示 900 秒（15 分钟）内有 1 个更改，300 秒（5 分钟）内有 10 个更改以及 60 秒内有 10000 个更改。<br>
 maxclients 128|设置同一时间最大客户端连接数，默认无限制，Redis 可以同时打开的客户端连接数为 Redis 进程可以打开的最大文件描述符数，如果设置 maxclients 0，表示不作限制。当客户端连接数到达限制时，Redis 会关闭新的连接并向客户端返回 max number of clients reached 错误信息 
vm-max-memory 0|将所有大于 vm-max-memory 的数据存入虚拟内存，无论 vm-max-memory 设置多小，所有索引数据都是内存存储的(Redis 的索引数据 就是 keys)，也就是说，当 vm-max-memory 设置为 0 的时候，其实是所有 value 都存在于磁盘。默认值为 0 


## 2. redis的数据结构
Redis支持五种数据类型：string（字符串），hash（哈希），list（列表），set（集合）及zset(sorted set：有序集合)。

注意：如果redis里面不同类型的，使用了同一个key值，则会报错。
```
127.0.0.1:6379> set lca "helloworld"
OK
127.0.0.1:6379> lpush lca redis
(error) WRONGTYPE Operation against a key holding the wrong kind of value
127.0.0.1:6379>
```

注意：Redis支持多个数据库，并且每个数据库的数据是隔离的不能共享，并且基于单机才有，如果是集群就没有数据库的概念。

Redis是一个字典结构的存储服务器，而实际上一个Redis实例提供了多个用来存储数据的字典，客户端可以指定将数据存储在哪个字典中。这与我们熟知的在一个关系数据库实例中可以创建多个数据库类似，所以可以将其中的每个字典都理解成一个独立的数据库。

每个数据库对外都是一个从0开始的递增数字命名，Redis默认支持16个数据库（可以通过配置文件支持更多，无上限），可以通过配置databases来修改这一数字。客户端与Redis建立连接后会自动选择0号数据库，不过可以随时使用SELECT命令更换数据库，如要选择1号数据库：
```
redis> SELECT 1
OK
redis [1] > GET foo
(nil)
```
然而这些以数字命名的数据库又与我们理解的数据库有所区别。首先Redis不支持自定义数据库的名字，每个数据库都以编号命名，开发者必须自己记录哪些数据库存储了哪些数据。另外Redis也不支持为每个数据库设置不同的访问密码，所以一个客户端要么可以访问全部数据库，要么连一个数据库也没有权限访问。最重要的一点是多个数据库之间并不是完全隔离的，比如FLUSHALL命令可以清空一个Redis实例中所有数据库中的数据。综上所述，这些数据库更像是一种命名空间，而不适宜存储不同应用程序的数据。比如可以使用0号数据库存储某个应用生产环境中的数据，使用1号数据库存储测试环境中的数据，但不适宜使用0号数据库存储A应用的数据而使用1号数据库B应用的数据，不同的应用应该使用不同的Redis实例存储数据。由于Redis非常轻量级，一个空Redis实例占用的内在只有1M左右，所以不用担心多个Redis实例会额外占用很多内存。

### 2.1 string
- string 是 redis 最基本的类型，你可以理解成与 Memcached 一模一样的类型，一个 key 对应一个 value。
- string 类型是二进制安全的。意思是 redis 的 string 可以包含任何数据。比如jpg图片或者序列化的对象。
- string 类型是 Redis 最基本的数据类型，string 类型的值最大能存储 **512MB**。 
```linux
127.0.0.1:6379> set lichangan 'niubi!'
OK
127.0.0.1:6379> get lichangan
"niubi!"
127.0.0.1:6379> 
```


### 2.2 hash
- Redis hash 是一个键值(key=>value)对集合。
- Redis hash 是一个 string 类型的 field 和 value 的映射表，hash 特别适合用于存储对象。
- 每个 hash 可以存储 2^32 -1 键值对（40多亿）。
- 命令：
	- 使用 Redis HMSET, HGET 命令，HMSET 设置了两个 field=>value 对, HGET 获取对应 field 对应的 value。

```
127.0.0.1:6379> hset lichangan name "李昌安" age  14 
(integer) 2
127.0.0.1:6379> 
127.0.0.1:6379> 
127.0.0.1:6379> 
127.0.0.1:6379> hgetall lichangan
1) "name"
2) "\xe6\x9d\x8e\xe6\x98\x8c\xe5\xae\x89"
3) "age"
4) "14"
127.0.0.1:6379> hget lichangan age
"14"
127.0.0.1:6379>
```

### 2.3 list
- Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）
- 列表最多可存储 2^32 - 1 元素 (4294967295, 每个列表可存储40多亿)。
- 命令：
	- **使用lpush**新建一个key来存储list元素
	- **使用lrange**命令遍历list的对象

```
127.0.0.1:6379> lpush lichangan redis
(integer) 1
127.0.0.1:6379> lpush lichangan nginx
(integer) 2
127.0.0.1:6379> lpush lichangan docker
(integer) 3
127.0.0.1:6379> lpush lichangan supervisor
(integer) 4
127.0.0.1:6379> lpush lichangan kafka
(integer) 5
127.0.0.1:6379> lpush lichangan rabbitmq
(integer) 6
127.0.0.1:6379> lrange lichangan
(error) ERR wrong number of arguments for 'lrange' command
127.0.0.1:6379> lrange lichangan 0 10
1) "rabbitmq"
2) "kafka"
3) "supervisor"
4) "docker"
5) "nginx"
6) "redis"
127.0.0.1:6379>
```

### 2.4 set
- 添加一个 string 元素到 key 对应的 set 集合中，成功返回 1，如果元素已经在集合中返回 0。
- 如果一个元素被添加两次，根据集合内元素的唯一性，第二次插入的元素将被忽略。
- 集合中最大的成员数为 232 - 1(4294967295, 每个集合可存储40多亿个成员)。 
- 命令：
	- 使用sadd来创建或者添加元素进set
	- 使用smembers来查看set内的元素
```
127.0.0.1:6379> sadd lichangan redis
(integer) 1
127.0.0.1:6379> sadd lichangan nginx
(integer) 1
127.0.0.1:6379> sadd lichangan docker
(integer) 1
127.0.0.1:6379> sadd lichangan redis
(integer) 0
127.0.0.1:6379> 
127.0.0.1:6379> smembers lichangan
1) "redis"
2) "docker"
3) "nginx"
127.0.0.1:6379>
```

### 2.5 zset
- Redis zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。
- 不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。
- zset的成员是唯一的,但分数(score)却可以重复。如果分数重复的话，会以首字母排序的方式进行排序。
- 注意如果member一样，但是score变更的时候，返回值是0，但是实际上score会被更新
- 命令，注意这里是zadd不是sadd：
	- zadd key score member 
	- zrange key start stop 进行遍历
	- zrangebyscore key start stop 进行排序遍历

```shell
127.0.0.1:6379> zadd lichangan 0 redis
(integer) 1
127.0.0.1:6379> zadd lichangan 1 nginx 
(integer) 1
127.0.0.1:6379> zadd lichangan 1 flask
(integer) 1
127.0.0.1:6379> zadd lichangan 2 docker
(integer) 1
127.0.0.1:6379> zadd lichangan 2 kafka
(integer) 1

# 如果score与member都相同，那么这个set会被忽略
127.0.0.1:6379> zadd lichangan 2 kafka
(integer) 0

# 如果member一样，但是score不一样，虽然返回值是0，但是score会被更新
127.0.0.1:6379> zadd lichangan 1 kafka
(integer) 0
127.0.0.1:6379> zrangebyscore lichangan 0 1000
1) "redis"
2) "flask"
3) "kafka"
4) "nginx"
5) "docker"

# score相同的情况下，默认以首字母的方式进行排序。
127.0.0.1:6379> zadd lichangan 0 a
(integer) 1
127.0.0.1:6379> zadd lichangan 0 b
(integer) 1
127.0.0.1:6379> zrangebyscore lichangan 0 1000 
1) "a"
2) "b"
3) "kafka"
4) "redis"
5) "flask"
6) "nginx"
7) "docker"
```


## 3. redis的发布订阅模式和频道
## 4. redis数据备份
## 5. redis解决的分布式问题
## 6. redis集群
