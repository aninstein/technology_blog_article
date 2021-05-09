# Docker笔记
---
---
## Docker安装
### 1. centos8.0安装Docker
```shell
yum update

# 设置镜像地址
yum install -y yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装依赖
yum install -y yum-utils device-mapper-persistent-data lvm2

# 手动安装containerd.io
yum install -y https://mirrors.aliyun.com/docker-ce/linux/centos/7/x86_64/edge/Packages/containerd.io-1.2.6-3.3.el7.x86_64.rpm

# 安装docker
yum install -y docker-ce

# 设置docker开机启动
systemctl enable docker

# 启动docker
systemctl start docker
```
## Docker介绍
### 1. 名词解释
- **镜像（Image）**：Docker 镜像（Image），就相当于是一个 root 文件系统。比如官方镜像 ubuntu:16.04 就包含了完整的一套 Ubuntu16.04 最小系统的 root 文件系统。
- **容器（Container）**：镜像（Image）和容器（Container）的关系，就像是面向对象程序设计中的类和实例一样，镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、停止、删除、暂停等。
- **仓库（Repository）**：仓库可看成一个代码控制中心，用来保存镜像。

我们使用镜像来创建容器，类似于类与对象的关系
### 2. 容器的相关概念
|概念|说明|
|:--|:--|
Docker 镜像(Images)|Docker 镜像是用于创建 Docker 容器的模板，比如 Ubuntu 系统。
Docker 容器(Container)|容器是独立运行的一个或一组应用，是镜像运行时的实体。
Docker 客户端(Client)|Docker 客户端通过命令行或者其他工具使用 Docker SDK (https://docs.docker.com/develop/sdk/) 与 Docker 的守护进程通信。
Docker 主机(Host)|一个物理或者虚拟的机器用于执行 Docker 守护进程和容器。
Docker Registry|Docker 仓库用来保存镜像，可以理解为代码控制中的代码仓库。
Docker Hub(https://hub.docker.com) 提供了庞大的镜像集合供使用。|一个 Docker Registry 中可以包含多个仓库（Repository）；每个仓库可以包含多个标签（Tag）；每个标签对应一个镜像。通常，一个仓库会包含同一个软件不同版本的镜像，而标签就常用于对应该软件的各个版本。我们可以通过 <仓库名>:<标签> 的格式来指定具体是这个软件哪个版本的镜像。如果不给出标签，将以 latest 作为默认标签。
Docker Machine|Docker Machine是一个简化Docker安装的命令行工具，通过一个简单的命令行即可在相应的平台上安装Docker，比如VirtualBox、 Digital Ocean、Microsoft Azure。
Docker Compose |Compose 是用于定义和运行多容器 Docker 应用程序的工具。通过 Compose，您可以使用 YML 文件来配置应用程序需要的所有服务。然后，使用一个命令，就可以从 YML 文件配置中创建并启动所有服务。
Swarm 集群管理|Docker Swarm 是 Docker 的集群管理工具。它将 Docker 主机池转变为单个虚拟 Docker 主机。 Docker Swarm 提供了标准的 Docker API，所有任何已经与 Docker 守护程序通信的工具都可以使用 Swarm 轻松地扩展到多个主机。
Kubernetes|Kubernetes是Google开源的一个容器编排引擎，它支持自动化部署、大规模可伸缩、应用容器化管理。在生产环境中部署一个应用程序时，通常要部署该应用的多个实例以便对应用请求进行负载均衡。在Kubernetes中，我们可以创建多个容器，每个容器里面运行一个应用实例，然后通过内置的负载均衡策略，实现对这一组应用实例的管理、发现、访问，而这些细节都不需要运维人员去进行复杂的手工配置和处理。

## Docker使用
### 1. hello world
我们使用Nginx的镜像来进行测试。由于我们之前已经把源换成了nginx，因此速度会快一些
```shell
# 查看docker源仓库中是否有nginx
docker search nginx


# 从仓库拉取nginx
docker pull nginx:latest

# 查看本地镜像就能够得到docker配置
docker images

# 运行容器，docker run是创建一个容器的命令，可以使用man docker run查看命令详解和参数
docker run --name nginx-test -p 8080:80 -d nginx

# 想要进入了docker的bash
docker exec -itd nginx /bin/bash

```
docker run常用参数：
-  --name nginx-test：容器名称。
- -p 8080:80： 端口进行映射，将本地 8080 端口映射到容器内部的 80 端口。
- -d nginx： 设置容器在在后台一直运行。
-  -v $PWD(本地目录):/python(容器目录) python /bin/bash ： 挂载本地路径到容器上
-  --rm bba-208 容器退出时就能够自动清理容器内部的文件系统

此时就能够通过访问，就能够访问nginx的首页了，即hello world
```
http://192.168.x.x:8080
```

### 2. 阿里云加速
使用docker镜像阿里云加速（注意改一下your accelerate address）：
```
sudo cp -n /lib/systemd/system/docker.service /etc/systemd/system/docker.service

sudo sed -i "s|ExecStart=/usr/bin/docker daemon|ExecStart=/usr/bin/docker daemon --registry-mirror=<your accelerate address>|g" /etc/systemd/system/docker.service

sudo sed -i "s|ExecStart=/usr/bin/dockerd|ExecStart=/usr/bin/dockerd --registry-mirror=<your accelerate address>|g" /etc/systemd/system/docker.service

sudo systemctl daemon-reload
sudo systemctl restart docker          
```
如上的配置是把/lib/systemd/system/docker.service配置进行了配置，会导致配置冲突，在配置成功之后，需要把原先的/lib/systemd/system/docker.service进行备份才能成功重启docker


关于文中的加速器地址\<your accelerate address>，请登录[容器镜像服务控制台](https://cr.console.aliyun.com/?spm=a2c4g.11186623.2.8.19e676277GKh0p)，在左侧导航栏选择镜像工具 > 镜像加速器，在镜像加速器页面的操作指引中查看，如下所示，也可以直接执行下面的配置，临时的使用加速，系统重启后就不行了。
```
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://2zytu2c0.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```
即\<your accelerate address>为：https://2zytu2c0.mirror.aliyuncs.com

## Dockerfile
dockerfile主要是构建自己的docker镜像的时候，用的的文件，实际上就是把构建一个docker镜像里面运行的环境使用了的命令全部罗列出来，然后逐行执行，最终生成一个系统镜像快照。

## Docker部署