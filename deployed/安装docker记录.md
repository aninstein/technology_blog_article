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

