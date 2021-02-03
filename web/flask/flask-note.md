# flask学习笔记
---
---
## 1. 搭建环境
### 1.1 使用pipenv
使用pipenv搭建虚拟环境，来代替原来的virtualenv+requirement.txt的方式，完成虚拟环境的搭建。
在项目的根目录，安装虚拟环境命令，随后会生成==Pipfile==文件与==Pipfile.lock==文件：
```
pip install pipenv
```
执行命令之后，在会在~/.local/share/virtualenvs/目录下创建虚拟环境文件夹

- ==pipenv install== 创建虚拟环境
- ==pipenv shell== 显示激活虚拟环境
- ==pipenv run== 如pipenv run python hello.py，可以用虚拟环境运行hello.py
- 与传统的requirement.txt手动维护的依赖包不同，pipenv在install之后会产生一个Pipfile文件
- ==pipenv graph== 查看依赖情况
- ==pipenv install \<pkg>== 安装pip包到虚拟环境，可以使用此命令安装flask：==pipenv install flask==
- ==pipenv update== 更新python包
- ==exit== 退出环境

由于需要使用pipenv安装python依赖包，换成国内镜像，则修改Pipfile文件中的==url==为国内源，如换成清华的源：
```
[[source]]
name = "pypi"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
verify_ssl = true
```
### 1.2 使用virtualenv
由于pipenv还是一个在不断完善中的虚拟环境管理工具，因此有可能有Lock效率低的风险，使用比较成熟的==virtualenv==也可以创建虚拟环境
```shell
# 安装virtualenv
pip install virtualenv

# 在app目录下创建一个虚拟环境
virtualenv venv

# 用source激活virtualenv环境
source venv/bin/activate

# 取消激活状态
deactivate
```
使用virtualenv需要在激活目录下放置一个依赖包的集合文件==requirement.txt==
我们初始化一个virtualenv环境的时候，默认只是安装一个最简单的python环境，想要默认安装更多的第三方包，可以通过拓展脚本的方式进行添加。


### 1.3 使用virtualenvwrapper
virtualenvwrapp是virtualenv功能的拓展，有如下用途：
- 用来管理全部的虚拟环境
- 方便的创建删除和拷贝虚拟环境
- 用单个命令就可以切换不同的虚拟环境
- 可以用那个Tab补全虚拟环境
- 支持用户粒度的钩子
安装：
```
pip install virtualenvwrapper
```
初始化virtualenvwrapper
```
export WORKON_HOME=~/venv
source /usr/local/bin/vitualenvwrapper.sh
```

## 2. hello world
### 2.1 hello world代码如下
代码文件'run_app.py'
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world！"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1234, debug=True)
```
### 2.2 flask代码开发服务器
#### 2.2.1 直接通过python运行
```
python run_app.py
```
#### 2.2.2 使用flask内置的测试服务器启动
注意：文件名称默认必须是‘app.py’或者‘wsgi.py’，可以通过==FLASK_APP==字段设置运行文件名称
比如'run_app.py'：
```
export FLASK_APP=run_app
```
不同的app可能有不同的环境变量，则可以使用python-dotenv管理环境变量，我们这里使用的pipenv，普通环境就使用pip即可
```
pipenv install python-dotenv
```
安装了python-dotenv在项目的根目录下，简历两个环境变量文件：.env和.flaskenv，.env用于存放项目私有配置，.flaskenv用于存放项目普通配置，环境变量优先级：手动设置变量>.env变量>.flaskenv变量

常用变量包括：
```
FLASK_APP=run_app
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=1234
FLASK_ENV=development/production

# 不建议手动设置
FLASK_DEBUG=1
```

flask run默认只开启127.0.0.1，端口是5000
```
flask run
```
#### 2.2.3 验证
在浏览器输入：
```
http://127.0.0.1:1234
```

#### 2.2.4 代码调试与重加载
在flask开启了debug之后，会有==werkzeug==可以进行代码自动加载，和使用PIN码在浏览器页面进行调试，为了加快重载速度，还可以安装==watchdog==，但注意仅限在开发环境：
```
pipenv install watchdog --dev
```

### 2.3 flask配置变量
flask的一些固定变量可以在==app.config==中配置，注意，键值必须是完全大写的。

## 3. 登陆页面
### 3.1 http相关知识
#### 3.1.1  状态码：使用状态码方法abort()
- 100，信息
	- 101，重连接
- 200，成功
	- 201，已创建。成功请求并创建了新的资源
	- 202，已接受。已经接受请求，但未处理完成
	- 203，非授权信息。请求成功。但返回的meta信息不在原始的服务器，而是一个副本
- 300，重定向
	- 301，永久移动
	- 302，临时移动
- 400，请求错误
	- 400，客户端请求的语法错误，服务器无法理解
	- 401，请求要求用户的身份认证
	- 403，服务器理解请求客户端的请求，但是拒绝执行此请求
	- 404，服务器无法根据客户端的请求找到资源（网页）。通过此代码，网站设计人员可设置"您所请求的资源无法找到"的个性页面
	- 405，客户端请求中的方法被禁止
	- 408，服务器等待客户端发送的请求时间过长，超时
	- 409，服务器完成客户端的 PUT 请求时可能返回此代码，服务器处理请求时发生了冲突
	- 415，服务器无法处理请求附带的媒体格式
- 500，服务端错误
	- 502，作为网关或者代理工作的服务器尝试执行请求时，从远程服务器接收到了一个无效的响应
	- 505，服务器不支持请求的HTTP协议的版本，无法完成处理

#### 3.1.2 content type
标识文件类型的，一般就是“text/html”、“image/png”等等
常见了类型有：
- text/plain：纯文本
- text/html：html文本
- application/xml：xml文本，仅仅传递数据而不提供渲染标签
- application/json：字典格式，只传输数据，我们一般用json进行数据交互，在flask中可以使用==jsonify==函数进行python字典序列化

1. 返回错误数据
```python
@app.route("/test")
def testhtml():
    return jsonify(message='Error!'), 500
```
2. 返回字典数据
```python
@app.route("/test")
def testhtml():
    ret_data = {"name": "lichangan", "gender": "male"}
    return jsonify(ret_data)
```
2. 返回参数数据
```python
@app.route("/test")
def testhtml():
    return jsonify(name="lichangan", gender="male")
```

#### 3.1.3 请求方式
- ==GET==请求：获取资源，GET操作幂等
- ==HEAD==请求：也是获取信息，但是只关心小洗头，应用应该像GET请求一样处理，但是不返回实际内容
- ==POST==请求：创建一个新的资源
- ==PUT==请求：完整的替换一个新的资源或者创建资源。操作应该是幂等的，但是可能会有副作用
- ==DELETE==请求：删除资源，支持批量删除，操作做应该是幂等的，但是可能会有副作用
- ==OPTIONS==请求：获取该资源支持的所有HTTP方法
- ==PATCH==请求：局部更新，修改某个已有的资源

ps：幂等，多次执行与执行一次的结果是一致的

### 3.2 Cookie
Cookie是web服务器存储的某个以key/value存放数据格式的空间，在flask中添加cookie最简便的方法就是直接使用set_cookie的方法在Response类中返回cookie
1. 先用make_response()构造一个响应对象，实际上是实例化内置的Response类
- header：一个Werkezeug的Header对象，响应的首部，可以像字典一样使用
- status：状态码，文本
- status_code：状态码，整型
- mimetype：MIME类型，只包括内容类型部分
	- 参考：http://www.lichangan.com/blog_article/mimetype.html
- set_cookie()：设置一个cookie

### 3.3 Session


## 4. 表单验证
## 5. 前后台交互
## 6. mysql数据集合
### 6.1 centos安装mysql
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

### 6.2 使用flask的migrate迁移数据库
需要先写db的orm的model表格，如：
```python
db = SQLAlchemy()


class User(db.Model):
    """
    用户表结构
    """
    __tablename__ = 'blog_user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    # 因为有用户名登录选项，所以此处必须唯一
    username = db.Column(db.String(64), index=True, unique=True, comment='用户名')
    name = db.Column(db.String(32), comment='真实姓名')
    password = db.Column(db.String(128), comment='密码，加密保存')
    email = db.Column(db.String(120), index=True, unique=True, comment='注册邮箱')
    location = db.Column(db.String(64), comment='居住地')
    slogan = db.Column(db.String(64), server_default='就命运而言，休论公道。', comment='Slogan')
    create_date = db.Column(db.DateTime(), default=datetime.utcnow, comment='用户创建时间')
    last_login = db.Column(db.DateTime(), default=datetime.utcnow, comment='最近登录时间')
    confirmed = db.Column(db.Boolean, default=False, comment='注册确认')
    avatar_hash = db.Column(db.String(32), comment='头像')
    articles = db.relationship('Article')
```

我们需要设置数据库的URL链接，在flask的app的config中，可以设置==SQLALCHEMY_DATABASE_URI==字段，为数据库的URL：
```python
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user_name@location:3306/database_name?charset=utf8mb4'
```

当然，这个我们一般很少这么直接赋值，因为每一个开发的产品一般都分为开发环境、测试环境、生产环境，真的不不通的环境我们一般用不同的配置内容，我们一般使用的
```python
app.config.from_object(config_obj)
```
这其中的config_obj是针对不同的环境的配置类，比如开发环境的配置类：
```python
class DevelopmentConfig(Config):
    DEBUG = True
    database = 'sex_code_blog_dev'
    SQLALCHEMY_DATABASE_URI = MySQLConfig.get_uri(database)
	···
```
然后我们在代码里面需要对这个app和上面的表格的db今次那个migrate的类的创建，其实就是一次注册。
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)  # 必须是在db被创建之后调用
```
但是仅仅只是这么写，只能够生成数据库表格并不能够生成的数据库本身，因此我们需要对Migrate进行改装一下，即如果数据库不存在，先创建数据库：
```python
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database
class MyMigrate(Migrate):

    def __init__(self, app=None, db=None, directory='migrations', **kwargs):
        self.app = app
        self.create_database()
        super(MyMigrate, self).__init__(app=self.app, db=db, directory=directory, **kwargs)

    def create_database(self):
        """
        如果不存在数据库，会先创建数据库
        :return:
        """
        db_uri = self.app.config['SQLALCHEMY_DATABASE_URI']
        engine = sqlalchemy.create_engine(db_uri)
        if not database_exists(engine.url):
            create_database(engine.url)
```


这样配置了mysql之后，就可以通过flask的migrate进行数据库迁移，当然也可以使用这个东西完成数据库的创建。

到app文件所在的那个目录，执行下面的命令
```shell
flask db init
flask db migrate -m "随便写点什么"
flask db upgrade
```
就能够完成数据库以及数据库表格的创建。


## 7. 安全能力
## 8. 部署方式
## 9. 高可用
## 10. 前端
使用nodejs管理包，使用vue进行前端的编写。我们测试时候一般使用==npm run dev==就可以，但是如果要上传到服务器的话就需要打包，使用==npm run build==对前端代码进行打包，最打包的tar文件上传到服务器，并且进行解压。
```linux
sudo unzip -d ./dist dist.zip       # 根据压缩包格式决定使用命令
sudo chown -R root:root dist        # 根据nginx中的配置确定
```
我们一般把静态
