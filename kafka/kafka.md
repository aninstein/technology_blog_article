# Kafka学习手册
---

本文摘自：
链接：[https://www.orchome.com/5](https://www.orchome.com/5)
来源：OrcHome

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
kafka可以使用本地的zookeeper，可以在server.properties配置文件中配置zookeeper的地址当然一般都使用kafka自带的zookeeper脚本执行


## 2. 安装kafka
1. 先启动zookeeper服务器：
```
bin/zookeeper-server-start.sh config/zookeeper.properties &
```

2. 然后启动kafka：
```
bin/kafka-server-start.sh config/server.properties &
```

3. 使用ps查看服务已经起来了：
```
ps -ef|grep kafka
```

4. 创建topic
```
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic lichangan-test
```
- zookeeper: 设置zookeeper的位置
- replication-factor：设置副本数是1
- partitions：设置这个topic有3个分区
- topic：设置topic名称

可以使用topic命令查看都有哪些topic
```
bin/kafka-topics.sh --list --zookeeper localhost:2181
```


5. 创建生产者
使用kafka命令：
```
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic lichangan-test
```
- broker-list：指定kafka节点列表
- topic：生产消息发往的topic
就会进入一个命令交互页面，我们换一个终端窗口，建立消费者

6. 创建消费者
使用以下命令创建消费者
```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic lichangan --from-beginning
```
- bootstrap-server：指定kafka节点
- topic：消费的topic
- from-beginning：从最初开始消费，即每次启动consumer的时候都会从头开始消费，如果没有这个字段，则从consumer起来的当前发送的消息开始消费

7. 发送数据
只要在producer的交互页面输入内容，consumer就能够打印出来




## 3. kafka概念
### 3.1 基本概念
- producer：消息的生产 者，向kafka的一个topic发送消息
- consumer：消息的消费者，订阅kafka的topic
- consumer group：对于一个topic，可以把消息广播给多个group，但是一个group只有一个consumer会消费到数据
- broker（物理概念）：实际上就是kafka中的一个kafka节点，就是kafka程序所在的服务器
- topic（逻辑概念）：其实就是kafka消息的类别，对数据进行分区和隔离
- partation（物理概念）：kafka下的数据存储单元。一个topic的数据会被分分散存储到多个partation，每一个partation都是有序的。kafka会把一个partation放在一个broker内。Kafka中采用partation的设计有几个目的。一是可以处理更多的消息，不受单台服务器的限制。Topic拥有多个partation意味着它可以不受限的处理更多的数据。第二，partation可以作为并行处理的单元。
	- 每一个topic被切分为多个partations
	- 消费者数目小于或者等于partation的数目
	- broker group中的每一个broke保存topic的一个或者多个partation，也就是说一个partation不会被多个broker保存。
	- 当一个partation非常大的时候，能够被多个broker共同存储这个partation，这种情况，每个broker保存的数据并不一样，也就是说依旧是一个partation并不会同时存在多个broker上。
	- consumer group中仅有一个consumer读取一个topic的一个或者多个partation，并且是唯一的consumer，主要是避免一个partation被多个consumer消费
- replication：同一个partation下可能有多个replica，每一个replica的数据是一样的。
	- 当集群中有broker挂掉的时候，系统可以主动的找replicas提供服务
	- 系统默认设置每一个topic的replication的系数为1，即默认不建立副本，可以在创建topic的时候单独设置
	- replication的基本单位是topic的partation
	- 所有的读和写都是从leader进，followers只是做备份
	- followers必须能够及时复制leader的数据
	- 增加容错性和可扩展性
- replication leader：再多个replica的中由replication leader负责该partation对producer与consumer交互。
- replicaManager：负责管理当前broker所有分区和副本的信息，处理kafkaController发起的一些请求，副本状态的切换、添加、读取消息等。

### 3.2 kafka Api
- producer API：发布消息到1个或多个topic（主题）中。
- consumer API：来订阅一个或多个topic，并处理产生的消息
- streams API：充当一个流处理器，从1个或多个topic消费输入流，并生产一个输出流到1个或多个输出topic，有效地将输入流转换到输出流
- connectors API：可构建或运行可重用的生产者或消费者，将topic连接到现有的应用程序或数据系统。例如，连接到关系数据库的连接器可以捕获表的每个变更

### 3.3 kafka消息格式
![kafka消息格式](images/1.jpg)

kafka消息字段：
- offset：记录当前消息的偏移
- length：消息有多长
- CRC32：校验消息的完整性
- magic：判定消息是不是kafka消息，如果这个magic的值和设定的不一致，那么可以快速的判定这个消息是不是当前kafka的
- attributes：可选，可以放一些属性字段，枚举值
- timestamp：时间戳
- key length：key长度
- key：key，没有长度限制
- value length：value长度
- value：value没有长度限制

### 3.4 kafka的特点
- 分布式
	- 多分区
	- 多副本
	- 多订阅者
	- 基于zookeeper调度的
- 高性能
	- 高吞吐量
	- 低延迟
	- 高并发
	- 时间复杂度O(1)
- 持久性和拓展性
	- 数据可持久化
	- 容错性能，多副本等
	- 支持在线水平拓展
	- 消息自动平衡：消息过于集中的访问某几台机器


## 4. kafka的应用场景
1. 消息队列，主要是点对点
2. 行为跟踪，发布订阅的扩展模式
3.  云信息监控，主要是操作信息，运维审计
4.  日志收集，比如ELK，HDFS等去做日志数据。用kafka可以做日志流。
5.  流处理，使用原始topic进行汇聚处理，处理完之后再发布到一个新的topic里，类似strom
6.  事件源：将状态转移按照时间序列进行排列，以实现状态回溯
7.  持久性日志（commit log），主要是使用日志回溯，让数据能够恢复

### 4.1 消息模型
一般来说，消息模型主要分为两种：
- 队列: 队列的处理方式是 一组消费者从服务器读取消息，一条消息只有其中的一个消费者来处理。

- 发布-订阅式: 消息被广播给所有的消费者，接收到消息的消费者都可以处理此消息。

但是kafka解决上述两种消息模型，统一使用消费者组（consumer group）实现。
- 队列：所有的消费则都在一个消费者组内
- 发布订阅：理想情况，一个消费者只在一个消费者组中


更通用的是，每个消费者组会有两个到多个消费者，一个组内多个消费者可以用来扩展性能和容错。
如下：

![2个kafka集群托管4个分区（P0-P3），2个消费者组，消费组A有2个消费者实例，消费组B有4个。](./images/consumer_group.png)


## 4.2 保证消息的顺序不变
Kafka保证消息的顺序不变，像传统的队列模型保持消息，并且保证它们的先后顺序不变。但是kafka是在kafka服务器上保证了消息的顺序不变，还是异步的发送给了各个消费者，消费者收到消息的先后顺序不能保证了。这也意味着并行消费将不能保证消息的先后顺序。如果只让一个消费者处理消息，又违背了并行处理的初衷。
在这一点上Kafka做的更好，尽管并没有完全解决上述问题。 Kafka采用了一种分而治之的策略：分区（partation）。 因为**Topic的partation中消息只能由消费者组中的唯一一个消费者处理，并确保消费者是该partition的唯一消费者，并按顺序消费数据。**，所以消息肯定是按照先后顺序进行处理的。但是它也**仅仅是保证Topic的一个分区顺序处理**，不能保证跨分区的消息先后处理顺序。 **所以，如果你想要顺序的处理Topic的所有消息，那就只提供一个分区。** 每个topic有多个分区，则需要对多个消费者做负载均衡。
**但请注意，相同的消费者组中不能有比分区更多的消费者，否则多出的消费者一直处于空等待，不会收到消息。**


- 生产者发送到一个特定的Topic的分区上，消息将会按照它们发送的顺序依次加入，也就是说，如果一个消息M1和M2使用相同的producer发送，M1先发送，那么M1将比M2的offset低，并且优先的出现在日志中。
- 消费者收到的消息也是此顺序。
- 如果一个Topic配置了复制因子（replication factor）为N， 那么可以允许N-1服务器宕机而不丢失任何已经提交（committed）的消息。


kafka中消费者组有两个概念：
- 队列：消费者组（consumer group）允许同名的消费者组成员瓜分处理。
- 发布订阅：允许你广播消息给多个消费者组（不同名）。

kafka的每个topic都具有这两种模式。

## 4.3 kafka的存储和流数据：
### 4.3.1 作为存储系统
Kafka是一个非常高性能的存储系统，写入到kafka的数据将写到磁盘并复制到集群中保证容错性。并允许生产者等待消息应答，直到消息完全写入。kafka的磁盘结构 - 无论你服务器上有50KB或50TB，执行是相同的。
client来控制读取数据的位置。你还可以认为kafka是一种专用于高性能，低延迟，提交日志存储，复制，和传播特殊用途的**分布式文件系统**。

### 4.3.2 作为流数据处理
仅仅读，写和存储是不够的，kafka的目标是实时的流处理。

在kafka中，流处理持续获取输入topic的数据，进行处理加工，然后写入输出topic。例如，一个零售APP，接收销售和出货的输入流，统计数量或调整价格后输出。

可以直接使用producer和consumer API进行简单的处理。对于复杂的转换，Kafka提供了更强大的Streams API。可构建聚合计算或连接流到一起的复杂应用程序。

助于解决此类应用面临的硬性问题：
- 1. 处理无序的数据
- 2. 代码更改的再处理
- 3. 执行状态计算等。

Streams API在Kafka中的核心：使用producer和consumer API作为输入，利用Kafka做状态存储，使用相同的组机制在stream处理器实例之间进行容错保障。

