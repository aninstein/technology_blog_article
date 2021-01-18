# Nginx问题汇总
---
---

## 1. 请解释一下什么是Nginx?
【答案】Nginx是一个web服务器和反向代理服务器，用于HTTP、HTTPS、SMTP、POP3和IMAP协议。
【解释】
- web服务器，即在服务端接收和响应也来自浏览器的http请求的
- 反向代理服务器：代理的意思是“我帮你”，正向代理即A要访问B的时候，由于A和B不互通，但是C可以访问B，因此C可以作为A的代理服务器，这里面清楚的知道要访问的资源是B，所以就叫正向代理；反向代理则是我有一个服务器集群，即我对外提供服务的时候，对外需要一个反向代理服务器，把访问资源的请求具体分发到某一台服务器上，这个过程我们并不知道是哪一台服务器来对我们服务。
- 其实主要是用于TCP连接相关的协议，但是Nginx也支持UDP的转发和负载均衡。


## 2. 请列举Nginx的一些特性
【答案】Nginx服务器的特性包括：
1. 反向代理
2. L7负载均衡器
3. 嵌入式Perl解释器
4. 动态二进制升级，即平滑升级
5. 动静分离
6. 可用于重新编写URL，具有非常好的PCRE支持

【解释】对于上述的特性，并不是Nginx独有
1. 现在最简单最好用的反向代理服务器还是Nginx
2. L7的负载均衡器，实际上，当不同业务需求，我们也可以使用L4的负载均衡配置。
	 - 所谓七层负载均衡，也称为“内容交换”，也就是主要通过报文中的真正有意义的应用层内容，再加上负载均衡设备设置的服务器选择方式，决定最终选择的内部服务器。
	 - 所谓四层负载均衡，也就是主要通过报文中的目标地址和端口，再加上负载均衡设备设置的服务器选择方式，决定最终选择的内部服务器。
3. 嵌入式Perl解释器，但是并没有Python解释器。如果对于一个绝大部分内容是静态的网站，只有极少数的地方需要动态显示，碰巧你又了解一点perl知识，那么nginx + perl的结合就能很好解决问题。
4. Nginx支持二进制文件直接替换然后完成升级，也可以在运行时候完成模块的添加操作。Nginx使用Unix信号机制来触发这一功能，更新命令为：
```linux
kill -USR2 `cat /usr/local/nginx/nginx.pid`

kill -QUIT `cat /usr/local/nginx/nginx.pid.oldbin`
```

在Nginx源码目录下，文件ngx_config.h中有以下代码：
```c++
#define NGX_CHANGEBIN_SIGNAL     USR2

#define NGX_SHUTDOWN_SIGNAL      QUIT
```
因为文件/usr/local/nginx/nginx.pid中保存的是当前Nginx进程pid，所以:
- 第一条命令旨在告诉Nginx二进制文件改变了，Nginx会将/usr/local/nginx/nginx.pid重命名为/usr/local/nginx/nginx.pid.oldbin。
- 第二条命令旨在通知Nginx老进程从容地退出。
 
 5. 动静分离，Nginx可以通过对不同的配置内容来区分动态资源和静态资源的访问路径
- 静态资源： 当用户多次访问这个资源，资源的源代码永远不会改变的资源。
- 动态资源：当用户多次访问这个资源，资源的源代码可能会发送改变。

为什么动静分离：
动静分离将网站静态资源（HTML，JavaScript，CSS，img等文件）与后台应用分开部署，提高用户访问静态代码的速度，降低对后台应用访问。这里我们将静态资源放到nginx中，动态资源转发到tomcat服务器中。

6. URL重写
URL重写是指将一个URL请求重新写成网站可以处理的另一个URL的过程。这样说可能不是很好理解，举个例子来说明一下，在开发中可能经常遇到这样的需求，比如通过浏览器请求的http://localhost:8080/getUser?id=1，但是需要通过SEO优化等等原因，需要把请求的地址重写为http://localhost:8080/getUser/1这样的URL，从而符合需求或者更好的被网站阅读。


## 3. 请列举Nginx和Apache 之间的不同点


## 4. 请解释Nginx如何处理HTTP请求。

Nginx使用反应器模式。主事件循环等待操作系统发出准备事件的信号，这样数据就可以从套接字读取，在该实例中读取到缓冲区并进行处理。单个线程可以提供数万个并发连接。

## 5. 在Nginx中，如何使用未定义的服务器名称来阻止处理请求?

只需将请求删除的服务器就可以定义为：

Server {

listen 80;

server_name “ “ ;

return 444;

}

这里，服务器名被保留为一个空字符串，它将在没有“主机”头字段的情况下匹配请求，而一个特殊的Nginx的非标准代码444被返回，从而终止连接。

## 6. 使用“反向代理服务器”的优点是什么?

反向代理服务器可以隐藏源服务器的存在和特征。它充当互联网云和web服务器之间的中间层。这对于安全方面来说是很好的，特别是当您使用web托管服务时。

## 7. 请列举Nginx服务器的最佳用途。

Nginx服务器的最佳用法是在网络上部署动态HTTP内容，使用SCGI、WSGI应用程序服务器、用于脚本的FastCGI处理程序。它还可以作为负载均衡器。

## 8. 请解释Nginx服务器上的Master和Worker进程分别是什么?

Master进程：读取及评估配置和维持

Worker进程：处理请求

## 9. 请解释你如何通过不同于80的端口开启Nginx?

为了通过一个不同的端口开启Nginx，你必须进入/etc/Nginx/sites-enabled/，如果这是默认文件，那么你必须打开名为“default”的文件。编辑文件，并放置在你想要的端口：

Like server { listen 81; }

## 10. 请解释是否有可能将Nginx的错误替换为502错误、503?

502 =错误网关

503 =服务器超载

有可能，但是您可以确保fastcgi_intercept_errors被设置为ON，并使用错误页面指令。

Location / {

fastcgi_pass 127.0.01:9001;

fastcgi_intercept_errors on;

error_page 502 =503/error_page.html;

#…

## 11. 在Nginx中，解释如何在URL中保留双斜线?

要在URL中保留双斜线，就必须使用merge_slashes_off;

语法:merge_slashes [on/off]

默认值: merge_slashes on

环境: http，server

## 12. 请解释ngx_http_upstream_module的作用是什么?

ngx_http_upstream_module用于定义可通过fastcgi传递、proxy传递、uwsgi传递、memcached传递和scgi传递指令来引用的服务器组。

## 13. 请解释什么是C10K问题?

C10K问题是指无法同时处理大量客户端(10,000)的网络套接字。

## 14. 请陈述stub_status和sub_filter指令的作用是什么?

Stub_status指令：该指令用于了解Nginx当前状态的当前状态，如当前的活动连接，接受和处理当前读/写/等待连接的总数

Sub_filter指令：它用于搜索和替换响应中的内容，并快速修复陈旧的数据

## 15. 解释Nginx是否支持将请求压缩到上游?

您可以使用Nginx模块gunzip将请求压缩到上游。gunzip模块是一个过滤器，它可以对不支持“gzip”编码方法的客户机或服务器使用“内容编码:gzip”来解压缩响应。

## 16. 解释如何在Nginx中获得当前的时间?

要获得Nginx的当前时间，必须使用SSI模块、$date_gmt和$date_local的变量。

Proxy_set_header THE-TIME $date_gmt;

## 17. 用Nginx服务器解释-s的目的是什么?

用于运行Nginx -s参数的可执行文件。

## 18. 解释如何在Nginx服务器上添加模块?

在编译过程中，必须选择Nginx模块，因为Nginx不支持模块的运行时间选择。