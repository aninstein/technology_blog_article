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

## 3. redis常用命令
### 3.1 键操作
- [dump key](http://redisdoc.com/internal/dump.html)：序列化key的操作，如果存在key则返回序列化后的值，如果不存在则返回空
```
127.0.0.1:6379> set lichangan "redis"
OK
127.0.0.1:6379> dump lichangan
"\x00\x05redis\t\x00\x15\xa2\xf8=\xb6\xa9\xde\x90"
127.0.0.1:6379> dump nokey
(nil)
127.0.0.1:6379>
```
[序列化的作用：https://www.gxlcms.com/redis-366739.html](https://www.gxlcms.com/redis-366739.html)
大概是：
序列化最终的目的是为了对象可以跨平台存储，和进行网络传输。而我们进行跨平台存储和网络传输的方式就是IO，而我们的IO支持的数据格式就是字节数组。 （推荐学习：Redis视频教程）

通过上面我想你已经知道了凡是需要进行“跨平台存储”和”网络传输”的数据，都需要进行序列化。

本质上存储和网络传输 都需要经过 把一个对象状态保存成一种跨平台识别的字节格式，然后其他的平台才可以通过字节信息解析还原对象信息。

- [EXPIRE key seconds](https://www.runoob.com/redis/keys-expire.html)：Redis Expire 命令用于设置 key 的过期时间，key 过期后将不再可用。单位以秒计。
- [PEXPIRE key milliseconds](https://www.runoob.com/redis/keys-pexpire.html)：设置 key 的过期时间以毫秒计。
```
127.0.0.1:6379> EXPIRE lichangan 10
(integer) 1
127.0.0.1:6379> exists lichangan
(integer) 1
127.0.0.1:6379> exists lichangan  # 10秒后
(integer) 0
127.0.0.1:6379>

```

- [EXPIREAT key timestamp](https://www.runoob.com/redis/keys-expireat.html)：Redis Expireat 命令用于以 UNIX 时间戳(unix timestamp)格式设置 key 的过期时间。key 过期后将不再可用。 
- [PEXPIREAT key milliseconds-timestamp](https://www.runoob.com/redis/keys-pexpireat.html)：设置 key 过期时间的时间戳(unix timestamp) 以毫秒计
```
127.0.0.1:6379> set lichangan redis
OK
127.0.0.1:6379> EXPIREAT lichangan 1615223284
(integer) 1
127.0.0.1:6379> exists lichangan
(integer) 0
127.0.0.1:6379>

```


- [TTL key](https://www.runoob.com/redis/keys-ttl.html)：以秒为单位，返回给定 key 的剩余生存时间(TTL, time to live)。当 key 不存在时，返回 -2 。 当 key 存在但没有设置剩余生存时间时，返回 -1 。 否则，以秒为单位，返回 key 的剩余生存时间。
- [PTTL key](https://www.runoob.com/redis/keys-pttl.html)：以毫秒为单位返回 key 的剩余的过期时间。当 key 不存在时，返回 -2 。 当 key 存在但没有设置剩余生存时间时，返回 -1 。 否则，以毫秒为单位，返回 key 的剩余生存时间。
- [PERSIST key](https://www.runoob.com/redis/keys-persist.html)：移除 key 的过期时间，key 将持久保持。
```
127.0.0.1:6379> pexpire lichangan 100000
(integer) 1
127.0.0.1:6379> pttl lichangan
(integer) 92740
127.0.0.1:6379> ttl lichangan
(integer) 86
127.0.0.1:6379> persist lichangan
(integer) 1
127.0.0.1:6379> ttl lichangan
(integer) -1
127.0.0.1:6379>
```


- [MOVE key db](https://www.runoob.com/redis/keys-move.html)：将当前数据库的 key 移动到给定的数据库 db 当中。移动成功返回 1 ，失败则返回 0 。 
```
127.0.0.1:6379> set lichangan redis
OK
127.0.0.1:6379> move lichangan 1
(integer) 1
127.0.0.1:6379> exists lichangan
(integer) 0
127.0.0.1:6379> select 1
OK
127.0.0.1:6379[1]> exists lichangan
(integer) 1
127.0.0.1:6379[1]>
```

- [TYPE key](https://www.runoob.com/redis/keys-type.html)
返回 key 所储存的值的类型。
```
127.0.0.1:6379> set lichangan redis
OK
127.0.0.1:6379> type lichangan
string
127.0.0.1:6379>
```

### 3.2 字符串操作
- SET key value
设置指定 key 的值
- GET key
获取指定 key 的值。
- GETRANGE key start end
返回 key 中字符串值的子字符
- GETSET key value
将给定 key 的值设为 value ，并返回 key 的旧值(old value)。
- GETBIT key offset
对 key 所储存的字符串值，获取指定偏移量上的位(bit)。
- MGET key1 [key2..]
获取所有(一个或多个)给定 key 的值。
- SETBIT key offset value
对 key 所储存的字符串值，设置或清除指定偏移量上的位(bit)。

- SETEX key seconds value
将值 value 关联到 key ，并将 key 的过期时间设为 seconds (以秒为单位)。
- SETNX key value
只有在 key 不存在时设置 key 的值。
```
redis 127.0.0.1:6379> SETEX mykey 60 redis
OK
redis 127.0.0.1:6379> TTL mykey
60
redis 127.0.0.1:6379> GET mykey
"redis
redis> EXISTS job                # job 不存在
(integer) 0
redis> SETNX job "programmer"    # job 设置成功
(integer) 1
redis> SETNX job "code-farmer"   # 尝试覆盖 job ，失败
(integer) 0
redis> GET job                   # 没有被覆盖
"programmer"
```
当我们使用redis处理分布式锁的问题的时候，一般会把setex和setnx连用，[解决分布式锁问题介绍](https://www.cnblogs.com/jiawen010/articles/11350125.html)
即通过setnx获取锁，如果能够获取到，则使用setex设置解锁时间。如果获取不到，则结束。


- SETRANGE key offset value
用 value 参数覆写给定 key 所储存的字符串值，从偏移量 offset 开始。
- STRLEN key
返回 key 所储存的字符串值的长度。
- MSET key value [key value ...]
同时设置一个或多个 key-value 对。
- MSETNX key value [key value ...]
同时设置一个或多个 key-value 对，当且仅当所有给定 key 都不存在。
- PSETEX key milliseconds value
这个命令和 SETEX 命令相似，但它以毫秒为单位设置 key 的生存时间，而不是像 SETEX 命令那样，以秒为单位。
- INCR key
将 key 中储存的数字值增一。
- INCRBY key increment
将 key 所储存的值加上给定的增量值（increment） 。
- INCRBYFLOAT key increment
将 key 所储存的值加上给定的浮点增量值（increment） 。
- DECR key
将 key 中储存的数字值减一。
- DECRBY key decrement
key 所储存的值减去给定的减量值（decrement） 。
- APPEND key value
如果 key 已经存在并且是一个字符串， APPEND 命令将指定的 value 追加到该 key 原来值（value）的末尾。 

### 3.3 哈希表操作
- HDEL key field1 [field2]
删除一个或多个哈希表字段
- HEXISTS key field
查看哈希表 key 中，指定的字段是否存在。
- HGET key field
获取存储在哈希表中指定字段的值。
- HGETALL key
获取在哈希表中指定 key 的所有字段和值
- HINCRBY key field increment
为哈希表 key 中的指定字段的整数值加上增量 increment 。
- HINCRBYFLOAT key field increment
为哈希表 key 中的指定字段的浮点数值加上增量 increment 。
- HKEYS key
获取所有哈希表中的字段
- HLEN key
获取哈希表中字段的数量
- HMGET key field1 [field2]
获取所有给定字段的值
- HMSET key field1 value1 [field2 value2 ]
同时将多个 field-value (域-值)对设置到哈希表 key 中。
- HSET key field value
将哈希表 key 中的字段 field 的值设为 value 。
- HSETNX key field value
只有在字段 field 不存在时，设置哈希表字段的值。
- HVALS key
获取哈希表中所有值。
- HSCAN key cursor [MATCH pattern] [COUNT count]
迭代哈希表中的键值对。

### 3.4 列表操作（list）
1. BLPOP key1 [key2 ] timeout
移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
如果列表为空，返回一个 nil 。 否则，返回一个含有两个元素的列表，第一个元素是被弹出元素所属的 key ，第二个元素是被弹出元素的值。

2.	BRPOP key1 [key2 ] timeout
移出并获取列表的最后一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
假如在指定时间内没有任何元素被弹出，则返回一个 nil 和等待时长。 反之，返回一个含有两个元素的列表，第一个元素是被弹出元素所属的 key ，第二个元素是被弹出元素的值。 

3.	BRPOPLPUSH source destination timeout
从列表中弹出一个值，将弹出的元素插入到另外一个列表中并返回它； 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
假如在指定时间内没有任何元素被弹出，则返回一个 nil 和等待时长。 反之，返回一个含有两个元素的列表，第一个元素是被弹出元素的值，第二个元素是等待时长。 


4.	LINDEX key index
通过索引获取列表中的元素，你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。 

6.	5.	LINSERT key BEFORE|AFTER pivot value
在列表的元素前或者后插入元素，列表的元素前或者后插入元素。当指定元素不存在于列表中时，不执行任何操作。
当列表不存在时，被视为空列表，不执行任何操作。
如果 key 不是列表类型，返回一个错误。 


6.	LLEN key
获取列表长度，返回列表的长度。 如果列表 key 不存在，则 key 被解释为一个空列表，返回 0 。 如果 key 不是列表类型，返回一个错误。 


7.	LPOP key
移出并获取列表的第一个元素，列表的第一个元素。 当列表 key 不存在时，返回 nil 


8.	LPUSH key value1 [value2]
将一个或多个值插入到列表头部，命令将一个或多个值插入到列表头部。 如果 key 不存在，一个空列表会被创建并执行 LPUSH 操作。 当 key 存在但不是列表类型时，返回一个错误。 

9.	LPUSHX key value
将一个值插入到已存在的列表头部，列表不存在时操作无效。 


10.	LRANGE key start stop
获取列表指定范围内的元素，区间以偏移量 START 和 END 指定。 其中 0 表示列表的第一个元素， 1 表示列表的第二个元素，以此类推。 你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。 


11	.LREM key count value
移除列表元素。
参数 COUNT 的值，移除列表中与参数 VALUE 相等的元素。

COUNT 的值可以是以下几种：
- count > 0 : 从表头开始向表尾搜索，移除与 VALUE 相等的元素，数量为 COUNT 。
- count < 0 : 从表尾开始向表头搜索，移除与 VALUE 相等的元素，数量为 COUNT 的绝对值。
- count = 0 : 移除表中所有与 VALUE 相等的值。


12.	LSET key index value
通过索引设置列表元素的值当索引参数超出范围，或对一个空列表进行 LSET 时，返回一个错误。

13.	LTRIM key start stop
对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。
下标 0 表示列表的第一个元素，以 1 表示列表的第二个元素，以此类推。 你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。

14.	RPOP key
移除列表的最后一个元素，返回值为移除的元素。当列表不存在时，返回 nil 。 


15.	RPOPLPUSH source destination
移除列表的最后一个元素，并将该元素添加到另一个列表并返回
16.	RPUSH key value1 [value2]
在列表中添加一个或多个值。如果列表不存在，一个空列表会被创建并执行 RPUSH 操作。 当列表存在但不是列表类型时，返回一个错误。
注意：在 Redis 2.4 版本以前的 RPUSH 命令，都只接受单个 value 值。

17.	RPUSHX key value
命令用于将一个值插入到已存在的列表尾部(最右边)。如果列表不存在，操作无效。 


### 3.5 集合操作（set）
1.	SADD key member1 [member2]
向集合添加一个或多个成员
2.	SCARD key
获取集合的成员数
3.	SDIFF key1 [key2]
返回第一个集合与其他集合之间的差异。也可以认为说第一个集合中独有的元素。不存在的集合 key 将视为空集。
差集的结果来自前面的 FIRST_KEY ,而不是后面的 OTHER_KEY1，也不是整个 FIRST_KEY OTHER_KEY1..OTHER_KEYN 的差集。

4.	SDIFFSTORE destination key1 [key2]
返回给定所有集合的差集并存储在 destination 中。如果指定的集合 key 已存在，则会被覆盖。


5.	SINTER key1 [key2]
返回给定所有集合的交集。 不存在的集合 key 被视为空集。 当给定集合当中有一个空集时，结果也为空集(根据集合运算定律)。 

6.	SINTERSTORE destination key1 [key2]
返回给定所有集合的交集并存储在 destination 中。如果指定的集合已经存在，则将其覆盖。

7.	SISMEMBER key member
判断 member 元素是否是集合 key 的成员。如果成员元素是集合的成员，返回 1 。 如果成员元素不是集合的成员，或 key 不存在，返回 0 。


8.	SMEMBERS key
返回集合中的所有成员，不存在的集合 key 被视为空集合。 

9.	SMOVE source destination member
将 member 元素从 source 集合移动到 destination 集合。
- SMOVE 是原子性操作。
- 如果 source 集合不存在或不包含指定的 member 元素，则 SMOVE 命令不执行任何操作，仅返回 0 。否则， member 元素从 source 集合中被移除，并添加到 destination 集合中去。
- 当 destination 集合已经包含 member 元素时， SMOVE 命令只是简单地将 source 集合中的 member 元素删除。
- 当 source 或 destination 不是集合类型时，返回一个错误。
- 如果成员元素被成功移除，返回 1 。 如果成员元素不是 source 集合的成员，并且没有任何操作对 destination 集合执行，那么返回 0 

10.	SPOP key
移除集合中的指定 key 的一个或多个随机元素，移除后会返回移除的元素。
该命令类似 Srandmember 命令，但 SPOP 将随机元素从集合中移除并返回，而 Srandmember 则仅仅返回随机元素，而不对集合进行任何改动。
被移除的随机元素。 当集合不存在或是空集时，返回 nil 。 


11. SRANDMEMBER key [count]
返回集合中一个或多个随机数。

从 Redis 2.6 版本开始， Srandmember 命令接受可选的 count 参数：
- 如果 count 为正数，且小于集合基数，那么命令返回一个包含 count 个元素的数组，数组中的元素各不相同。如果 count 大于等于集合基数，那么返回整个集合。
- 如果 count 为负数，那么命令返回一个数组，数组中的元素可能会重复出现多次，而数组的长度为 count 的绝对值。 

该操作和 SPOP 相似，但 SPOP 将随机元素从集合中移除并返回，而 Srandmember 则仅仅返回随机元素，而不对集合进行任何改动。 
返回值：只提供集合 key 参数时，返回一个元素；如果集合为空，返回 nil 。 如果提供了 count 参数，那么返回一个数组；如果集合为空，返回空数组。 


12.	SREM key member1 [member2]
移除集合中一个或多个成员。命令用于移除集合中的一个或多个成员元素，不存在的成员元素会被忽略。
当 key 不是集合类型，返回一个错误。
返回值：被成功移除的元素的数量，不包括被忽略的元素。 

13.	SUNION key1 [key2]
返回所有给定集合的并集，不存在的集合 key 被视为空集。 
14.	SUNIONSTORE destination key1 [key2]
所有给定集合的并集存储在 destination 集合中。如果 destination 已经存在，则将其覆盖。
15.	SSCAN key cursor [MATCH pattern] [COUNT count]
迭代集合中的元素。Sscan 继承自 Scan。 
- SSCAN 命令用于迭代集合键中的元素。
- HSCAN 命令用于迭代哈希键中的键值对。
- ZSCAN 命令用于迭代有序集合中的元素（包括元素成员和元素分值）。
对于：
```
SSCAN key cursor [MATCH pattern] [COUNT count]
```
- cursor - 游标。
- pattern - 匹配的模式。
- count - 指定从数据集里返回多少元素，默认值为 10 。

### 3.6 有序集合操作（zset）
1.	ZADD key score1 member1 [score2 member2]
向有序集合添加一个或多个成员，或者更新已存在成员的分数
2.	ZCARD key
获取有序集合的成员数
3.	ZCOUNT key min max
计算在有序集合中指定区间分数的成员数
4.	ZINCRBY key increment member
有序集合中对指定成员的分数加上增量 increment。
可以通过传递一个负数值 increment ，让分数减去相应的值，比如 ZINCRBY key -5 member ，就是让 member 的 score 值减去 5 。
当 key 不存在，或分数不是 key 的成员时， ZINCRBY key increment member 等同于 ZADD key increment member 。当 key 不是有序集类型时，返回一个错误。
分数值可以是整数值或双精度浮点数。 

5.	ZINTERSTORE destination numkeys key [key ...]
计算给定的一个或多个有序集的交集并将结果集存储在新的有序集合 destination 中。给定的一个或多个有序集的交集，其中给定 key 的数量必须以 numkeys 参数指定，并将该交集(结果集)储存到 destination 。
默认情况下，结果集中某个成员的分数值是所有给定集下该成员分数值之和。 

6.	ZLEXCOUNT key min max
在有序集合中计算指定字典区间内成员数量
7.	ZRANGE key start stop [WITHSCORES]
通过索引区间返回有序集合指定区间内的成员
指定区间内的成员。
其中成员的位置按分数值递增(从小到大)来排序。
具有相同分数值的成员按字典序(lexicographical order )来排列。
如果你需要成员按
值递减(从大到小)来排列，请使用 ZREVRANGE 命令。
下标参数 start 和 stop 都以 0 为底，也就是说，以 0 表示有序集第一个成员，以 1 表示有序集第二个成员，以此类推。
你也可以使用负数下标，以 -1 表示最后一个成员， -2 表示倒数第二个成员，以此类推。 

8.	ZRANGEBYLEX key min max [LIMIT offset count]
通过字典区间返回有序集合的成员

9.	ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT]
Zrangebyscore 返回有序集合中指定分数区间的成员列表。有序集成员按分数值递增(从小到大)次序排列。
具有相同分数值的成员按字典序来排列(该属性是有序集提供的，不需要额外的计算)。
默认情况下，区间的取值使用闭区间 (小于等于或大于等于)，你也可以通过给参数前增加 ( 符号来使用可选的开区间 (小于或大于)。

10.	ZRANK key member
返回有序集合中指定成员的索引。其中有序集成员按分数值递增(从小到大)顺序排列。 如果成员是有序集 key 的成员，返回 member 的排名。 如果成员不是有序集 key 的成员，返回 nil 。 

11.	ZREM key member [member ...]
移除有序集合中的一个或多个成员。 不存在的成员将被忽略。当 key 存在但不是有序集类型时，返回一个错误。

12.	ZREMRANGEBYLEX key min max
移除有序集合中给定的字典区间的所有成员
13.	ZREMRANGEBYRANK key start stop
移除有序集合中给定的排名区间的所有成员
14.	ZREMRANGEBYSCORE key min max
移除有序集合中给定的分数区间的所有成员
15.	ZREVRANGE key start stop [WITHSCORES]
返回有序集中指定区间内的成员，通过索引，分数从高到低
16.	ZREVRANGEBYSCORE key max min [WITHSCORES]
返回有序集中指定分数区间内的成员，分数从高到低排序
17.	ZREVRANK key member
返回有序集合中指定成员的排名，有序集成员按分数值递减(从大到小)排序
18.	ZSCORE key member
返回有序集中，成员的分数值
19.	ZUNIONSTORE destination numkeys key [key ...]
计算给定的一个或多个有序集的并集，并存储在新的 key 中
20.	ZSCAN key cursor [MATCH pattern] [COUNT count]
迭代有序集合中的元素（包括元素成员和元素分值）


### 3.7 hyperLogLog
Redis HyperLogLog 是用来做基数统计的算法，HyperLogLog 的优点是，在输入元素的数量或者体积非常非常大时，计算基数所需的空间总是固定的、并且是很小的。

在 Redis 里面，每个 HyperLogLog 键只需要花费 12 KB 内存，就可以计算接近 2^64 个不同元素的基数。这和计算基数时，元素越多耗费内存就越多的集合形成鲜明对比。

但是，因为 HyperLogLog 只会根据输入元素来计算基数，而不会储存输入元素本身，所以 HyperLogLog 不能像集合那样，返回输入的各个元素。

- 什么是基数?
比如数据集 {1, 3, 5, 7, 5, 7, 8}， 那么这个数据集的基数集为 {1, 3, 5 ,7, 8}, 基数(不重复元素)为5。 基数估计就是在误差可接受的范围内，快速计算基数。 

- 常用命令：
1.	PFADD key element [element ...]
添加指定元素到 HyperLogLog 中。
2.	PFCOUNT key [key ...]
返回给定 HyperLogLog 的基数估算值。
3.	PFMERGE destkey sourcekey [sourcekey ...]
将多个 HyperLogLog 合并为一个 HyperLogLog 

### 3.8 Redis GEO

Redis GEO 主要用于存储地理位置信息，并对存储的信息进行操作，该功能在 Redis 3.2 版本新增。

Redis GEO 操作方法有：

- geoadd：添加地理位置的坐标。
- geopos：获取地理位置的坐标。
- geodist：计算两个位置之间的距离。
- georadius：根据用户给定的经纬度坐标来获取指定范围内的地理位置集合。
- georadiusbymember：根据储存在位置集合里面的某个地点获取指定范围内的地理位置集合。
- geohash：返回一个或多个位置对象的 geohash 值。



## 4. redis的发布订阅模式和频道
### 4.1 redis的订阅模式
#### 4.1.1 键空间通知
首先需要熟悉，什么是redis键空间通知。
我们可以在redis执行，开启键空间通知。
```
config set notify-keyspace-events Ex
```

   Redis的键空间通知(keyspace notifications)功能是自2.8.0版本开始加入的，客户端可以通过订阅/发布(Pub/Sub)机制，接收那些以某种方式改变了Redis数据空间的事件通知。比如：所有改变给定key的命令；所有经过lpush操作的key；所有在0号数据库中过期的key等等。

通知是通过Redis的订阅/发布机制发送的，因此，所有支持订阅/发布功能的客户端都可在无需调整的情况下，使用键空间通知功能。

Redis的发布/订阅目前是即发即弃(fire and forget)模式的，因此无法实现事件的可靠通知。也就是说，如果发布/订阅的客户端断链之后又重连，则在客户端断链期间的所有事件都丢失了。

#### 4.1.2 发布订阅模式介绍
Redis 发布订阅 (pub/sub) 是一种消息通信模式：发送者 (pub) 发送消息，订阅者 (sub) 接收消息。
Redis 客户端可以订阅任意数量的频道。

下图展示了频道 channel1 ， 以及订阅这个频道的三个客户端 —— client2 、 client5 和 client1 之间的关系：
![](https://www.runoob.com/wp-content/uploads/2014/11/pubsub1.png)
当有新消息通过 PUBLISH 命令发送给频道 channel1 时， 这个消息就会被发送给订阅它的三个客户端：
![](https://www.runoob.com/wp-content/uploads/2014/11/pubsub2.png)


- Redis 发布订阅命令

1.	PSUBSCRIBE pattern [pattern ...]
订阅一个或多个符合给定模式的频道。
2.	PUBSUB subcommand [argument [argument ...]]
查看订阅与发布系统状态。
3.	PUBLISH channel message
将信息发送到指定的频道。
4.	PUNSUBSCRIBE [pattern [pattern ...]]
退订所有给定模式的频道。
5.	SUBSCRIBE channel [channel ...]
订阅给定的一个或多个频道的信息。
6.	UNSUBSCRIBE [channel [channel ...]]
指退订给定的频道。


### 4.2 redis的频道与redis实现的消息队列
摘自：https://www.jianshu.com/p/d32b16f12f09
我们知道常用的消息队列有kafka，rabbitmq等。但是使用redis也能够实现消息队列。
redis实现消息队列的方式主要有：
1. 基于List的 LPUSH+BRPOP和键空间通知 的实现
2. PUB/SUB，订阅/发布模式
3. 基于Sorted-Set的实现
4. 基于Stream类型的实现

## 5. redis数据备份与迁移
redis数据备份的方式主要包括版持久化的RDB和全持久化的AOF

### 5.1 RDB（redis database）

通过快照完成，由用户在redis.conf配置文件中设置两个参数：时间和改动的键的个数。当在指定的时间内被更改的键的个数大于指定的数值时，redis会自动将内存中的所有数据进行快照并存储在硬盘上，完成数据备份。备份文件名称：dump.rdb
```
# 指定在多长时间内，有多少次更新操作，就将数据同步到数据文件，可以多个条件配合
# Redis 默认配置文件中提供了三个条件：

save <seconds> <changes>
save 900 1
save 300 10
save 60 10000
```
分别表示 900 秒（15 分钟）内有 1 个更改，300 秒（5 分钟）内有 10 个更改以及 60 秒内有 10000 个更改。

## 6. redis解决的分布式问题
## 7. redis集群


## 摘录自：
redis官方文档：http://redisdoc.com/topic/index.html
菜鸟教程：https://www.runoob.com/redis/redis-keys.html