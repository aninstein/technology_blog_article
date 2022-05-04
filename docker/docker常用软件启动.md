# docker常用软件启动

## 0. 加速
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

## 1. 启动mysql

```
docker run -itd --name mysql \
-e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 \
-v /usr/mydata/mysql/log:/var/log/mysql \
-v /usr/mydata/mysql/data:/media/mysql \
-v /usr/mydata/mysql/conf:/etc/mysql/conf.d \
--character-set-server=utf8 \
--collation-server=utf8_unicode_ci mysql:5.7
```

- docker run -d mysql:latest             以后台的方式运行 mysql 版本的镜像，生成一个容器。
- --name mysql                           容器名为 mysql
- -e MYSQL_ROOT_PASSWORD=123456          设置登陆密码为 123456，登陆用户为 root
- -p 3306:3306                           将容器内部 3306 端口映射到 主机的 3306 端口，即通过 主机的 3306 可以访问容器的 3306 端口
- -v /usr/mydata/mysql/log:/var/log/mysql    将容器的 日志文件夹 挂载到 主机的相应位置
- -v /usr/mydata/mysql/data/media/mysql   将容器的 数据文件夹 挂载到 主机的相应位置
- -v /usr/mydata/mysql/conf:/etc/mysql/conf.d   将容器的 自定义配置文件夹 挂载到主机的相应位置

12QGA8CuPI_F

## 2. 启动redis
## 3. 启动postgresql
## 4. 启动nginx
## 5. 启动flask
## 6. 启动django
## 7. 启动springboot
## 8. 启动tomcat
## 9. 启动kafka
## 10. 启动zookeeper
## 11. 启动rabbitmq