## 1. 安装docker
### 1.1 卸载旧版本
```linux
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```
### 1.2 安装依赖
```linux
sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
```
安装docker
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
