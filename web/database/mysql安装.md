# centos8安装mysql
---
---

## 安装mysql
```linux
yum install mysql mysql-server -y

```

配置数据库
```linux
vim /etc/my.cnf
```

添加这三行
```init
skip-grant-tables
character_set_server=utf8
init_connect='SET NAMES utf8'
```

启动mysql
```linux
# 开机自启动
systemctl enable mysqld.service

# 启动mysql
systemctl start mysqld.service
```

先进入mysql的数据库，查看user表格：
```linux
mysql> use mysql
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+---------------------------+
| Tables_in_mysql           |
+---------------------------+
| columns_priv              |
| component                 |
| db                        |
| default_roles             |
| engine_cost               |
| func                      |
| general_log               |
| global_grants             |
| gtid_executed             |
| help_category             |
| help_keyword              |
| help_relation             |
| help_topic                |
| innodb_index_stats        |
| innodb_table_stats        |
| password_history          |
| plugin                    |
| procs_priv                |
| proxies_priv              |
| role_edges                |
| server_cost               |
| servers                   |
| slave_master_info         |
| slave_relay_log_info      |
| slave_worker_info         |
| slow_log                  |
| tables_priv               |
| time_zone                 |
| time_zone_leap_second     |
| time_zone_name            |
| time_zone_transition      |
| time_zone_transition_type |
| user                      |
+---------------------------+
33 rows in set (0.01 sec)

mysql> select * from user;
···
```

因为user表字段太多了，我们需要查看mysql都有哪些字段，方便采取：
```linux
SHOW COLUMNS FROM user;
```

然后通过百度得知，mysql8已经不支持这么直接改密码了，于是放弃了。

继续百度通过==mysqladmin==修改密码

mysqladmin常用命令：
```
-c number 自动运行次数统计，必须和 -i 一起使用
-i number 间隔多长时间重复执行
每个两秒查看一次服务器的状态，总共重复5次。
./mysqladmin -uroot -p -i 2 -c 5 status
-h, --host=name Connect to host. 连接的主机名或iP
-p, --password[=name] 登录密码，如果不写于参数后，则会提示输入
-P, --port=# Port number to use for connection. 指定数据库端口
-s, --silent Silently exit if one can't connect to server.
-S, --socket=name Socket file to use for connection. 指定socket file
-i, --sleep=# Execute commands again and again with a sleep between. 间隔一段时间执行一次
-u, --user=name User for login if not current user.登录数据库用户名
-v, --verbose Write more information. 写更多的信息
-V, --version Output version information and exit. 显示版本
```

mysqladmin常用命令
```
mysqladmin password lichangan123                  #<==设置密码，前文用过的。
mysqladmin -uroot -plichangan123 password lichangan  #<==修改密码，前文用过的。
mysqladmin -uroot -plichangan123 status           #<==查看状态，相当于show status。
mysqladmin -uroot -plichangan123 -i 1 status      #<==每秒查看一次状态。
mysqladmin -uroot -plichangan123 extended-status   #<==等同show global status;。
mysqladmin -uroot -plichangan123 flush-logs        #<==切割日志。
mysqladmin -uroot -plichangan123 processlist       #<==查看执行的SQL语句信息。
mysqladmin -uroot -plichangan123 processlist -i 1  #<==每秒查看一次执行的SQL语句。
mysqladmin -uroot -p'lichangan' shutdown           #<==关闭mysql服务，前文用过的。
mysqladmin -uroot -p'lichangan' variables          #<==相当于show variables。
```

