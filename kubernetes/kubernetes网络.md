# kubernetes容器网络
---
---
## 1. 容器网络标准
### 1.1 CNM（container network model）
是docker提出的一种网络标准，Libnetwork是其中的一种实现
 
 docker的网络模块
 - 通过插件为docker提供网络功能
 - 创建容器的过程和网络是解耦的
 - 使得docker能够支持多种类型的网络

在docker定义的CNM三个组成部分：
- Endpoint：一个网络接口，实际上就是网卡，可用于某一网络上的交流。
	- veth pair
		- netdev设备
		- veth是成对出现的
- Network：Network 是一个唯一的且可识别的Endpoint组，为endpoint提供网络连接
- 网络沙箱（sandbox）：网络沙箱包含来自不同的network的endpoint，给endpoint提供网络协议栈，包括路由表、dns、网卡存放空间等

以上三个配置在对容器的inspect中都能看到：

在Networks中能看到：
```json
"Networks": {
                "composetest_default": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "composetest-web-1",
                        "web",
                        "da4c97371a60"
                    ],
                    "NetworkID": "8e2035cc3c6fb3a16625dd13cb4f550451f175cdbc9e49c9b6bc95616614db25",
                    "EndpointID": "e9777a29d03a6dbc3b5a5fd3b44503fd2c94f9fa98c110bf9a4d19696185c117",
                    "Gateway": "172.18.0.1",
                    "IPAddress": "172.18.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:12:00:02",
                    "DriverOpts": null
                }
            }
```
且字段
```
"SandboxKey": "/var/run/docker/netns/2cc47b200ed4",
```



### 1.2 CNI（container network interface）
