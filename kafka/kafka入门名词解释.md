# Kafka入门名词解释
---
---
### 1. 基本概念
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

## 2. kafka相关概念
### 2.1 分布式(Distribution)
Log的分区被分布到集群中的多个服务器上。每个服务器处理它分到的分区。 根据配置每个分区还可以复制到其它服务器作为备份容错。 每个分区有一个leader，零或多个follower。Leader处理此分区的所有的读写请求，而follower被动的复制数据。如果leader宕机，其它的一个follower会被推举为新的leader。 一台服务器可能同时是一个分区的leader，另一个分区的follower。 这样可以平衡负载，避免所有的请求都只让一台或者某几台服务器处理。


### 2.2 Geo-Replication(异地数据同步技术)
Kafka MirrorMaker为群集提供geo-replication支持。借助MirrorMaker，消息可以跨多个数据中心或云区域进行复制。 您可以在active/passive场景中用于备份和恢复; 或者在active/passive方案中将数据置于更接近用户的位置，或数据本地化。