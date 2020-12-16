# cookie和session的关系
---

* [cookie和session的关系](#cookie和session的关系)
	* [定义](#定义)
	* [存储](#存储)
	* [联系](#联系)

---

## 定义

- Cookie，有时也用其复数形式 Cookies，指某些网站为了辨别用户身份、进行 session 跟踪而储存在用户本地终端上的数据（通常经过加密）
- Session：在计算机中，尤其是在网络应用中，称为“会话控制”。Session对象存储特定用户会话所需的属性及配置信息。
cookie和session本质的区别是，**一个位于客户端，一个位于服务端**。这个特性带着浓重的色彩，实际中的应用都离不开这个定义。

## 存储
### （1）cookie的存储
这里仅仅针对浏览器中的cookie来讨论，如果抛开其他特性来说，cookie本质上是浏览器（http请求）提供的一种客户端存储的数据，但是这个存储数据有自己的一些特性，比如：cookie长度的限制，跨域的限制（当然可以在服务端配合的情况下的突破这种限制）等。
就像所有的存储一样，cookie也可以保存在内存中，也可以保存在磁盘中，只不过保存在磁盘的时候是在浏览器的存储目录下，毕竟cookie是基于http的，http请求又基于浏览器。

### （2）session的存储
session即会话，本质上是一种服务端的存储数据。
诞生的主要原因是为了解决http无状态这种特性。既然是数据，其实就可以存储于任何介质中，像实际应用中，有存储于内存中的，也有存储于redis的。所以只要看透了它的本质，存储在哪里可能就只是一个驱动的问题了。

## 联系
### cookie
当用户第一次访问并登陆一个网站的时候，cookie的设置以及发送会经历以下4个步骤：
1. 客户端发送一个请求到服务器
2. 服务器发送一个HttpResponse响应到客户端，其中包含Set-Cookie的头部
3. 客户端保存cookie，之后向服务器发送请求时，HttpRequest请求中会包含一个Cookie的头部
4. 服务器返回响应数据
```linux
set-cookie: session=4a0b9b1cce73c469b8a6b6a8aec294d5; domain=.xx.com; path=/; expires=Sun, 25 Aug 2019 08:21:27 -0000; secure; HttpOnly
```
以上过程是一个最常见的场景，cookie的特性以及值是由服务端来下发，但是**cookie本质上是一种客户端技术，所以客户端其实同样能操作cookie**，比如：
登录的时候服务端的返回结果中可以不包含set-cookie的头部，而是把值通过正文来返回，客户端脚本通过读取返回的正文解析出结果，然后写入cookie同样能达到相同的效果。
set-cookie只不过是http协议中已经约定好的格式，服务端告诉客户端需要设置cookie的协议而已。当然cookie还有其他很多特性（可能随着发展有所增加或者减少）：

|属性	|介绍|
|:--|:--|
name|	name字段为一个cookie的名称
value|	value字段为一个cookie的值
domain|	可以访问此cookie的域名
path|	可以访问此cookie的页面路径
expires/Max-Age	|此cookie超时时间。
Size|	Size字段 此cookie大小
http|	cookie的httponly属性
secure|	设置是否只能通过https来传递此条cookie
由于浏览器的安全策略，不同域名的cookie是不允许的，但是可以通过服务端的配置可以解决这个问题。即[跨域问题](https://zhuanlan.zhihu.com/p/28562290)

### session

session的创建目的初衷就是为了让服务端记住会话，简而言之就是让服务端能识别出来是哪个客户端，既然要记住，那服务端必须要存储每个会话的数据，比如：实际项目中最常用的用户信息等。
服务端存储这些用户数据没问题，最大的一个障碍是怎么样识别诸多请求中哪些是同一个会话。要解决这个问题，只依靠服务端无法解决，必须需要客户端来配合：**需要上传==会话的标识==**。

- 会话标识
客户端上传会话的标识，必须是客户端和服务端都能支持的协议和数据，其实也可以看做是http请求支持的协议和数据，既然是基于http请求，最方便的就是利用cookie，cookie是一种key-value的数据存储格式，value的值正适合作为session的标识（session也是一种key-value的存储），在这种情况下cookie终于和session有了一定的联系。

session机制利用cookie来作为标识的传输机制，并不意味着只能用cookie，只要是服务端和客户端约定好了位置，session标识我可以放到http请求的任何位置（当然http请求必须得支持传输才可以）。你完全可以把session的标识放到http头Authorization字段，只要服务端能正确的读到此值并且正确解析即可。

有些面试官喜欢问cookie和session的相同和不同，甚至他们的联系，这样的提问在某种程度上是不太好的，容易让人错误的认为cookie和session的联系很密切，但是其实cookie和session之间没有太大关系，主要分为：
- cookie中的session值是由后台生成的，返回到前台中
- session会理由cookie中的session-key找到对应存于服务器的的session信息