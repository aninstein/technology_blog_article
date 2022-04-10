# Docker进阶（3）docker compose
---

---
## 1. 容器编排
## 2. docker compose
### 2.1 安装
官网很慢：
```
curl -L "https://github.com/docker/compose/releases/download/v2.2.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

这里使用国内的网站下载：
```
curl -L https://get.daocloud.io/docker/compose/releases/download/v2.2.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
 
chmod +x /usr/local/bin/docker-compose

 ln -s /usr/local/bin/docker-compose /usr/bin/docker-compos
 
docker-compose --help
```

学习资源：
官网：https://docs.docker.com/compose/gettingstarted/
菜鸟：https://www.runoob.com/docker/docker-compose.html

### 2.2 官方文档创建一个简单的web应用
应用说明：
使用到了redis和flask搭建的一个简单的计数器引用程序：
```
mkdir composetest
cd composetest
```
在composetest创建一下文件：

- app.py

```python
# -*- coding: utf-8 -*-
import time

import redis
from flask import Flask

app = Flask(__name__)
# 这里使用了docker network，所以host可以直接写redis
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

- requirements.txt
python环境的依赖包文件，用pip安装
```
flask
redis
```

- Dockerfile
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
ADD . /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

- docker-compose.yml
```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:5000"
  redis:
    image: "redis:alpine"
```

配置完后的目录结构：
```
[root@localhost composetest]# ll
总用量 16
-rw-r--r-- 1 root root 632 4月  10 23:48 app.py
-rw-r--r-- 1 root root 119 4月  10 23:49 docker-compose.yml
-rw-r--r-- 1 root root 299 4月  11 00:09 Dockerfile
-rw-r--r-- 1 root root  14 4月  10 23:49 requirements.txt
```
然后直接运行，以下为运行成功：
```
[root@localhost composetest]#
[root@localhost composetest]# docker-compose up
[+] Running 2/0
 ⠿ Container composetest-web-1    Created                                                                                       0.0s
 ⠿ Container composetest-redis-1  Created                                                                                       0.0s
Attaching to composetest-redis-1, composetest-web-1
composetest-redis-1  | 1:C 10 Apr 2022 16:11:10.389 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
composetest-redis-1  | 1:C 10 Apr 2022 16:11:10.389 # Redis version=6.2.6, bits=64, commit=00000000, modified=0, pid=1, just started
composetest-redis-1  | 1:C 10 Apr 2022 16:11:10.389 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.390 * monotonic clock: POSIX clock_gettime
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.391 * Running mode=standalone, port=6379.
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.391 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.391 # Server initialized
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.391 * Loading RDB produced by version 6.2.6
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.391 * RDB age 38 seconds
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.391 * RDB memory usage when created 0.79 Mb
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.391 # Done loading RDB, keys loaded: 1, keys expired: 0.
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.391 * DB loaded from disk: 0.000 seconds
composetest-redis-1  | 1:M 10 Apr 2022 16:11:10.391 * Ready to accept connections
composetest-web-1    |  * Serving Flask app 'app.py' (lazy loading)
composetest-web-1    |  * Environment: production
composetest-web-1    |    WARNING: This is a development server. Do not use it in a production deployment.
composetest-web-1    |    Use a production WSGI server instead.
composetest-web-1    |  * Debug mode: off
composetest-web-1    |  * Running on all addresses (0.0.0.0)
composetest-web-1    |    WARNING: This is a development server. Do not use it in a production deployment.
composetest-web-1    |  * Running on http://127.0.0.1:5000
composetest-web-1    |  * Running on http://172.18.0.2:5000 (Press CTRL+C to quit)
```

可以直接访问：
```
[root@localhost composetest]# curl localhost:8000
Hello World! I have been seen 1 times.
[root@localhost composetest]# curl localhost:8000
Hello World! I have been seen 2 times.
[root@localhost composetest]# curl localhost:8000
Hello World! I have been seen 3 times.
```

结束。

### 2.3 一个简单的