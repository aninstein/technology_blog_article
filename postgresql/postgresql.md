# postgresql
---
---

## 1. 安装postgresql
### 1.1 本地安装postgresql
配置repo，可以从postgresql官网上查看相关的repo链接：
https://yum.postgresql.org/packages/#pg11



```
# /etc/yum.repos.d/postgresql11.repo


[postgresql]
name=postgresql
baseurl=https://download.postgresql.org/pub/repos/yum/11/redhat/rhel-8.2-x86_64/
enabled=1
gpgcheck=0
```

直接yum（or dnf）安装数据库
```
dnf install postgresql-server postgresql-contrib postgresql-devel 
```

### 1.2 docker安装数据库
拉取postgresql镜像
```
docker pull postgres:11
```
构建docker容器：
```
mkdir -p /data
mkdir -p /data/pg_data

docker run -itd -v /data/pg_data/:/data -w /data -e POSTGRES_PASSWORD=password --net mynet --name pgserver -p 5432:5432 postgres:11


# 进入容器
docker exec -it pgserver bash

# 容器内
export　POSTGRES_HOST_AUTH_METHOD=trust
source /etc/profile
ldconfig
```
- -v /media/data/data/:/data，挂载卷
- -w /data，设置工作目录
- -e POSTGRES_PASSWORD=password，设置数据库密码为password
- --net mynet：使用自定义网络，这里选填，默认参数是docker0，[docker如何添加自定义网络](https://www.cnblogs.com/aaawei/p/13402289.html)
- --name pgserver，设置容器名称为pgserver
- -p 5432:5432，发布端口

当然新建容器之后，可以使用export添加新的一些环境变量，也可以使用--env-file设置多个参数。
```
POSTGRES_PASSWORD=password
POSTGRES_HOST_AUTH_METHOD=trust  # 把本机当做可信主机，不需要输入密码
```

进入容器之后，使用psql连接数据
```
psql -U postgres 
```

当然如果宿主机安装了postgresql-client，也可以在宿主机连接数据库
```
psql -U postgres -h 127.0.0.1 -p 5432
```


## 2. 创建数据库以及数据库表设计



```
```