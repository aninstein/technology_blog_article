# django学习笔记

---
---

## 1. 用docker部署django app
1. 使用centos的镜像
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
然后：
```
docker pull centos:centos7
```

2. django自动生成代码项目代码框架
```
django-admin startproject mysite
```

3. 生成并且进入容器
```
docker run -itd --name django_demo -v $PWD/mysite:/usr/src/mysite -w /usr/src/mysite -p 8000:8000 centos:centos7 /bin/bash


docker exec -it django_demo /bin/bash
```

4. 安装python3环境
直接yum安装
```
# 安装的是3.6的 
# yum install -y python3
```

源码安装
```
# 安装依赖包
yum install libffi-devel wget sqlite-devel xz gcc make atuomake zlib-devel openssl-devel epel-release gcc-c++  -y

# https://www.python.org/downloads/release/python-3912/
tar zxvf env-dep/Python-3.9.12.tgz -C env-dep/
cd env-dep/Python-3.9.12
./configure;make;make install
cd - > /dev/null
```

5. 安装项目依赖包
```
mkdir -p ~/.pip
cp env-dep/pip.conf ~/.pip/

pip3 install -r requirement.txt
```


使用python3.9：
```
# requirement.txt
asgiref==3.5.0
Django==4.0.3
django-grappelli==3.0.3
gevent==21.12.0
greenlet==1.1.2
gunicorn==20.1.0
Pillow==9.0.1
pip==21.2.4
ply==3.11
psycogreen==1.0.2
pycrypto==2.6.1
setuptools==58.1.0
sqlparse==0.4.2
zope.event==4.5.0
zope.interface==5.4.0
pysqlite3-binary==0.4.6
```

5. 安装sqlite

可以在sqlite官网看到比较新的下载连接：
最新版本：https://www.sqlite.org/download.html
历史版本：https://www.sqlite.org/changes.html

```
wget https://www.sqlite.org/2022/sqlite-autoconf-3380100.tar.gz
tar zxvf env-dep/sqlite-autoconf-3380100.tar.gz -C env-dep/
cd env-dep/sqlite-autoconf-3380100
./configure
make;make install
cd - > /dev/null

# 设置共享库路径：
export LD_LIBRARY_PATH="/usr/local/lib"
mv /usr/bin/sqlite3  /usr/bin/sqlite3_7
ln -s /usr/local/bin/sqlite3   /usr/bin/sqlite3

# 测试一下sqlite3更新成功
sqlite3 --vserion  # 输出 3.38.1

python -c "import sqlite3;print(sqlite3.sqlite_version)"  # 输出 3.38.1
```

安装完后发现太高版本也不支持：
```
Traceback (most recent call last):
  File "/usr/local/lib/python3.9/threading.py", line 973, in _bootstrap_inner
    self.run()
  File "/usr/local/lib/python3.9/threading.py", line 910, in run
    self._target(*self._args, **self._kwargs)
  File "/usr/local/lib/python3.9/site-packages/django/utils/autoreload.py", line 64, in wrapper
    fn(*args, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/django/core/management/commands/runserver.py", line 137, in inner_run
    self.check_migrations()
  File "/usr/local/lib/python3.9/site-packages/django/core/management/base.py", line 576, in check_migrations
    executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
  File "/usr/local/lib/python3.9/site-packages/django/db/migrations/executor.py", line 18, in __init__
    self.loader = MigrationLoader(self.connection)
  File "/usr/local/lib/python3.9/site-packages/django/db/migrations/loader.py", line 58, in __init__
    self.build_graph()
  File "/usr/local/lib/python3.9/site-packages/django/db/migrations/loader.py", line 235, in build_graph
    self.applied_migrations = recorder.applied_migrations()
  File "/usr/local/lib/python3.9/site-packages/django/db/migrations/recorder.py", line 81, in applied_migrations
    if self.has_table():
  File "/usr/local/lib/python3.9/site-packages/django/db/migrations/recorder.py", line 57, in has_table
    with self.connection.cursor() as cursor:
  File "/usr/local/lib/python3.9/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/base/base.py", line 284, in cursor
    return self._cursor()
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/base/base.py", line 260, in _cursor
    self.ensure_connection()
  File "/usr/local/lib/python3.9/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/base/base.py", line 244, in ensure_connection
    self.connect()
  File "/usr/local/lib/python3.9/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/base/base.py", line 244, in ensure_connection
    self.connect()
  File "/usr/local/lib/python3.9/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/base/base.py", line 225, in connect
    self.connection = self.get_new_connection(conn_params)
  File "/usr/local/lib/python3.9/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/django/db/backends/sqlite3/base.py", line 212, in get_new_connection
    create_deterministic_function(
django.db.utils.NotSupportedError: deterministic=True requires SQLite 3.8.3 or higher

```

- 解决方法1：
修改源码，替换为pysqlite3：
```
pip3 install  pysqlite3-binary

# 报错的源码
vim /usr/local/lib/python3.9/site-packages/django/db/backends/sqlite3/base.py

# 替换为pysqlite3
# from sqlite3 import dbapi2 as Database
from pysqlite3 import dbapi2 as Database
```
再启动django
```
python3 manage.py runserver 0.0.0.0:8000
```

- 解决方法2：
安装合适版本的sqlite，经过实验，合适版本的sqlite为：没有


## 2. 运行Django
### 2.1 运行
输入以下命令可以运行django的开发服务器
```
python3 manage.py runserver 0.0.0.0:8000
```
在页面输入虚拟机ip+端口即可访问django的欢迎页面（一个小火箭）


### 2.2 开发一个投票页面
剩下的步骤，可以按照官方文档的实验步骤，把一个投票应用：[编写你的第一个 Django 应用](https://docs.djangoproject.com/zh-hans/4.0/intro/tutorial01/)


### 2.3 我们使用postgresql代替django自带的sqlite
#### 2.3.1 安装数据库
具体查看postgresql数据库安装页面

#### 2.3.2 django使用postgresql数据库
参考自django官方文档：https://docs.djangoproject.com/zh-hans/4.0/ref/databases/#postgresql-notes

需要安装psycopg2
```

```

