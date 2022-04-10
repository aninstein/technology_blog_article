# Docker进阶（二）容器网络
---

---
## 1. 容器网络

思考问题：
1. docker是如何处理容器的网络访问的？

### 1.1 docker0
- docker0是docker安装时候自带的一个虚拟网卡，与物理网卡是属于nat关系。
- evth-pair技术，是一堆虚拟设备接口，他们是成对出现的，一段连着的协议，一段彼此相连的。正是因为有这个特性，evth-pair充当一个桥梁，连接各种虚拟网络设备

- --link，是使用的/etc/hosts做映射，因此容器互联需要相互配置，且IP变更了之后还是不能通过容器名称进行联通的，不建议使用。

### 1.2 docker network自定义网络
```
[root@localhost ~]# docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
fb2729c7eadc   bridge    bridge    local
109b6ccc0674   host      host      local
06d513d8bac7   none      null      local
```
- bridge：桥接（默认）
- none：不配置网络
- host：主机模式，和linux主机共享网络
- container：容器内网络联通，是容器直接互联

可以查看docker network有什么功能：
```
[root@localhost ~]# docker network --help

Usage:  docker network COMMAND

Manage networks

Commands:
  connect     Connect a container to a network
  create      Create a network
  disconnect  Disconnect a container from a network
  inspect     Display detailed information on one or more networks
  ls          List networks
  prune       Remove all unused networks
  rm          Remove one or more networks

Run 'docker network COMMAND --help' for more information on a command.
```
可以通过network创建一个网络，先看一下啊create参数应用：
```
[root@localhost ~]# docker network create --help

Usage:  docker network create [OPTIONS] NETWORK

Create a network

Options:
      --attachable           Enable manual container attachment
      --aux-address map      Auxiliary IPv4 or IPv6 addresses used by Network driver (default map[])
      --config-from string   The network from which to copy the configuration
      --config-only          Create a configuration only network
  -d, --driver string        Driver to manage the Network (default "bridge")
      --gateway strings      IPv4 or IPv6 Gateway for the master subnet
      --ingress              Create swarm routing-mesh network
      --internal             Restrict external access to the network
      --ip-range strings     Allocate container ip from a sub-range
      --ipam-driver string   IP Address Management Driver (default "default")
      --ipam-opt map         Set IPAM driver specific options (default map[])
      --ipv6                 Enable IPv6 networking
      --label list           Set metadata on a network
  -o, --opt map              Set driver specific options (default map[])
      --scope string         Control the network's scope
      --subnet strings       Subnet in CIDR format that represents a network segment
```

应用：
```
docker network create --driver bridge --subnet 192.168.0.0/16 --gateway 192.168.0.1  mynet
```

这样能够创建一个网络，通过docker network ls可以查看配置的子网
```
[root@localhost ~]# docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
fb2729c7eadc   bridge    bridge    local
109b6ccc0674   host      host      local
3c6d878c6b8f   mynet     bridge    local
06d513d8bac7   none      null      local
```
使用自定义网络，在创建容器分配地址的时候，就使用--net进行自定义网络即可
```
docker run -itd -v /data/pg_data/:/data -w /data -e POSTGRES_PASSWORD=password --net mynet --name pgserver -p 5432:5432 postgres:11
```

**而且自定义网络中自带了IP和域名的映射，可以通过容器名称访问容器**
即直接在别的docker中进行：
```
ping pgserver
```
可以成功ping

### 1.3 网络之间的联通
很容易可以联想到，创建的网络往往是有其功能作用的，比如docker部署redis和mysql的集群：
- redis: 划分网络172.24.18.0/24
- mysql: 划分网络172.24.17.0/24

一个网段内部肯定是可以互联互通的，但是让redis和mysql两个网段之间能互通，则需要进行配置网络间互通的配置。

联通一个容器到网络，可以从上面的network参数当中看到，connect的方式可以把容器连接到一个网络当中
```
[root@localhost ~]# docker network connect --help

Usage:  docker network connect [OPTIONS] NETWORK CONTAINER

Connect a container to a network

Options:
      --alias strings           Add network-scoped alias for the container
      --driver-opt strings      driver options for the network
      --ip string               IPv4 address (e.g., 172.30.100.104)
      --ip6 string              IPv6 address (e.g., 2001:db8::33)
      --link list               Add link to another container
      --link-local-ip strings   Add a link-local address for the container
```
我们按照上面操作先创建一个新的网络mynet02
```
docker network create --driver bridge --subnet 192.167.0.0/16 --gateway 192.167.0.1  mynet02
```
让上面的创建的容器pgserver能够连接到mynet当中
```
docker network connect mynet02 pgserver
```
然后查看网络mynet02即可看到pgserver容器已经在mynet02当中了

```
docker network inspect mynet02
```
注意：connect只能够实现某一个容器访问网络，如果想要多个容器能够访问这个网络，那么原则上属于网络规划问题。