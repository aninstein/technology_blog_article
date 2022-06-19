1.CNI环境介绍(Kubernetes 1.20.5)
2.常用CNI方案及相应落地概述
3.CNI设计原理通述
4.Wireshark抓包工具概述及应用
5.eNSP网络模拟器安装，介绍，应用

1.OSI七层和TCP/IP四层网络参考模型
2.IP知识及VLSM剖析
3.OSPF，BGP，Static基础路由知识
4.MAC，VLAN基础交换知识
5.大二层VxLAN网络技术介绍
6.通用IPIP/GENEVE数据封装
7.云化网络之虚拟网络

1.eBPF基础概念及原理
2.eBPF应用之tcpdump
3.eBPF应用之TC
4.eBPF应用之XDP
5.Linux DataPath中的Hook介绍

1.Cilium 1.11安装及TS
2.Cilium之Native Routing模式
3.Cilium之VxLAN模式
4.Cilium之BGP模式
5.Cilium网络方案总结

1.Cilium1.11Native Routing模式安装
2.同节点下不同Pod间通信
3.bfp_redirect_peer()helper函数应用
4.Pod名称空间及协议栈深入分析
5.eBPF Host-Routing分析
6.跨节点Pod间通信
7.Linux路由原理
8.bpf_redirect_neigh()helper函数应用
9.iptables/eBPF Code观察DataPath
10.pwru工具安装使用及观察DataPath
11.tcpdump工具观察DataPath
12.Native Routing Benchmark

1.Cilium1.11VxLAN模式安装
2.同节点下不同Pod间通信
3.bfp_redirect_peer()helper函数应用
4.Pod名称空间及协议栈深入分析
5.eBPF Host-Routing分析
6.跨节点Pod间通信
7.Linux VxLAN原理
8.bpf_redirect_neigh()helper函数应用
9.iptables/eBPF Code观察DataPath
10.pwru工具安装使用及观察DataPath
11.tcpdump工具观察DataPath
12.VxLAN模式 Benchmark
13.传统数据中心VxLAN架构分析
14.eNSP实现传统数据中心VxLAN抓包分析
15.eNSP实现传统数据中心之静态配置VxLAN Tunnel
16.eNSP实现传统数据中心之BGP EVPN配置VxLAN Tunnel

1.Cilium Host-Reachable Service[W-E traffic]
2.Cilium DSR[N-S traffic]
3.Cilium Identify
4.Cilium Network Masqurading
5.Cilium Streamlines the Service Mesh
6.Cilium eBPF(XDP) compare with DPDK
7.Cilium in teclcom industry
8.Cilium XDP多设备负载均衡

1.Cilium IPAM设计原理
2.Cilium IPAM with Cluster Scope
3.Cilium IPAM with kubernetes host scope
4.Cilium IPAM with CRD-Backend
5.通用IPAM设计逻辑

1.Calico IPIP模式
2.Calico VxLAN模式
3.Calico BGP模式
4.Calico VPP模式
5.Calico eBPF模式

1.Calico IPIP模式介绍
2.同节点Pod间通信逻辑
3.veth pair通信逻辑
4.Proxy ARP原理
5.跨节点Pod间通信
6.Linux实现IPIP通信
7.TUN和tunl设备原理分析
8.tcpdump抓包观察DataPath
9.IPIP模式结合(BGP)bird
10.IPIP模式整体通信逻辑分析
11.Calico IPIP模式Benchmak

1.Calico VxLAN模式介绍
2.同节点Pod间通信逻辑
3.跨节点Pod间通信
4.VxLAN模式设计原理
5.平滑迁移Flannel VxLAN模式

1.Calico BGP模式介绍
2.BGP基础原理介绍
3.IBGP 和 EBGP
4.eNSP BGP实战
5.BGP RR介绍
6.BGP 路由学习原则
7.BGP 生产环境演示
8.同节点Pod间通信
9.跨节点Pod间通信
10.BGP Full Mesh模式和RR模式
11.生产环境BGP网络剖析
12.生产环境网络架构对比
13.Calico Over Ethernet fabic模式
14.Calico Over IP fabic模式
15.AS Per RACK Model模式精讲
16.BGP模式总结

1.Calico VPP模式介绍
2.VPP基础
3.同节点Pod间通信
4.TUN设备在VPP模式下的应用
5.跨节点Pod间通信
6.VPP 数据包DataPath
7.生产环境中VPP专题
8.VPP with DPDK实现高性能网络
9.VPP 通用设计思路

1.Calico IPAM设计通解
2.Calico IPV4/IPV6 with calic-ipam 模式
3.Calico IPV4/IPV6 with host-local 模式
4.IPAM增强特性介绍

1.Flannel整体介绍
2.Flannel UDP模式
3.Flannel VxLAN模式
4.Flannel IPIP模式
5.Flannel host-gw模式
6.Flannel VxLAN & Directing Routing

1.Flannel UDP模式介绍
2.同节点Pod通信逻辑
3.跨节点Pod间通信
4.veth pair应用
5.Linux Bridge 和 OVS Bridge
6.Linux 数据通信剖析
7.基础交换路由知识
8.TAP和TUN设备应用及实践
9.UDP模式性能分析
10.tcpdump工具观察DataPath

1.Flannel VxLAN模式介绍
2.同节点Pod间通信
3.跨节点Pod间通信
4.点对点模式VXLAN实现
5.多播模式VxLAN实现
6.深入理解VxLAN应用场景
7.手工实现类Flannel网络

1.Flannel IPIP模式介绍
2.同节点Pod间通信
3.跨节点Pod间通信
4.对比Calico IPIP实现逻辑
5.Flannel IPIP模式 Benchmark

1.Flannel host-gw模式介绍
2.同节点Pod间通信
3.跨节点Pod间通信
4.深入剖析Linux数据包转发逻辑
5.host-gw模式Benchmark
6.Flannel VxLAN和Directing Routing模式应用

1.Flannel CNI Plugin
2.Flannel CNI Bridge Plugin
3.Flannel之CNI之IPAM通用模板
4.Flannel之CNI之IPAM[host-local] With IPV4
5.Flannel之CNI之IPAM[host-local] With IPV6

1.SRIOV基础架构
2.DPDK原理介绍
3.VPP原理介绍
4.高性能网络生产应用

1.SRIOV整体介绍
2.SRIOV之PF VF
3.CNI之srivo-cni
4.CNI之srivo-network-device-plugin
5.SRIOV驱动
6.内核bypass技术介绍
7.SRIOV技术在fastpath网络中应用

1.DPDK基本介绍
2.DPDK旁路原理
3.DPDK之UIO
4.DPDK之PMD
5.DPDK之HugePage
6.DPDK之NUMA
7.DPDK With VPP
8.VPP基本介绍
9.VPP基础设计原理
10.对比Calico VPP实现模式

1.电信领域通用解决方案
2.SRIOV VF资源介绍
3.DPDK资源介绍
4.DPDK-enabled APP
5.Multus(intel)集成多CNI
6.Multus mutiple 网络应用
7.高性能网络方案落地介绍

1.MACVLAN技术
2.IPVLAN技术
3.Multus加载多CNI
4.IPVLAN和MACVLAN场景应用区分
5.Mutiple CNI DANM方案落地
6.DANM(Nokia)CNI专题
6.DANM CNI落地
7.CNI Genie(Huawei)

1.IPAM通解
2.static IPAM介绍及应用
3.host-local IPAM介绍及应用
4.dhch IPAM介绍及应用
5.whereabouts 介绍
6.whereabouts结合mutiple CNI
7.IPAM应用场景

1.IPV6基本概念
2.IPV6报文格式
3.ICMPv6
4.IPV6邻居发现
5.IPV6在VPP中应用
6.CNI with IPV6
7.Kubernetes IPV6