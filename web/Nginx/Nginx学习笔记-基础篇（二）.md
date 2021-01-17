---
title:  Nginx学习笔记-基础篇（二）
tags: nginx,中间件,基础篇
grammar_abbr: true
grammar_table: true
grammar_defList: true
grammar_emoji: true
grammar_footnote: true
grammar_ins: true
grammar_mark: true
grammar_sub: true
grammar_sup: true
grammar_checkbox: true
grammar_mathjax: true
grammar_flow: true
grammar_sequence: true
grammar_plot: true
grammar_code: true
grammar_highlight: true
grammar_html: true
grammar_linkify: true
grammar_typographer: true
grammar_video: true
grammar_audio: true
grammar_attachment: true
grammar_mermaid: true
grammar_classy: true
grammar_cjkEmphasis: true
grammar_cjkRuby: true
grammar_center: true
grammar_align: true
grammar_tableExtra: true
--- 
---

---
## 1. HTTP请求头
查看http请求数据头
```linux
curl -v www.baidu,com
```
相应
```linux
[root@localhost learn_nginx]# curl -v www.baidu.com
* Rebuilt URL to: www.baidu.com/
*   Trying 110.242.68.4...
* TCP_NODELAY set
* Connected to www.baidu.com (110.242.68.4) port 80 (#0)
> GET / HTTP/1.1
> Host: www.baidu.com
> User-Agent: curl/7.61.1
> Accept: */*
> 
< HTTP/1.1 200 OK
< Accept-Ranges: bytes
< Cache-Control: private, no-cache, no-store, proxy-revalidate, no-transform
< Connection: keep-alive
< Content-Length: 2381
< Content-Type: text/html
< Date: Sun, 17 Jan 2021 08:32:09 GMT
< Etag: "588604c1-94d"
< Last-Modified: Mon, 23 Jan 2017 13:27:29 GMT
< Pragma: no-cache
< Server: bfe/1.0.8.18
< Set-Cookie: BDORZ=27315; max-age=86400; domain=.baidu.com; path=/
< 
<!DOCTYPE html>
<!-- ··· -->
</html>
* Connection #0 to host www.baidu.com left intact

```
上面的这个请求中，有包括：

- request请求
```linux
> GET / HTTP/1.1
> Host: www.baidu.com
> User-Agent: curl/7.61.1
> Accept: */*
```

- response参数
```linux
< HTTP/1.1 200 OK
< Accept-Ranges: bytes
< Cache-Control: private, no-cache, no-store, proxy-revalidate, no-transform
< Connection: keep-alive
< Content-Length: 2381
< Content-Type: text/html
< Date: Sun, 17 Jan 2021 08:32:09 GMT
< Etag: "588604c1-94d"
< Last-Modified: Mon, 23 Jan 2017 13:27:29 GMT
< Pragma: no-cache
< Server: bfe/1.0.8.18
< Set-Cookie: BDORZ=27315; max-age=86400; domain=.baidu.com; path=/
```

## 2. Nginx的日志
Nginx的log配置主要是两个配置：
- error.log：记录错误日志
```nginxconf
error_log /var/log/nginx/error.log warn;
```

- access.log：记录每一个HTTP请求的访问状态
```nginxconf
http{
    access_log  /var/log/nginx/access.log  main;
}
```

以上两个错误日志的日志格式都是由log_format来进行定义的，log_format的使用语法：
```nginxconf
log_format
Syntax log_format name ···
Default: log_format···
Content: http
```
log_format默认配置：
```nginxconf
http {
	    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
	    log_format "$remote_addr"  // log的日志格式，[$参数]是nginx的变量
        access_log <log路径> main
}
```

对于log_format都有的参数主要是以下三类：
- http请求的变量：arg-PARAMETER、http_HEADER、send_http_HEADER
	- request，是：$http_<HEADER的请求参数，且需要小写，“-”转换为下划线“_”\>
	- response，是：$send_http_<HEADER的请求参数，且需要小写，“-”转换为下划线“_”\>
- [Nginx内置变量](http://nginx.org/en/docs/http/ngx_http_log_module.html#log_format)：
- 自定义变量：


## 3. Nginx的模块
### 3.1 内置模块
我们在[Nginx基础篇（一）](https://blog.csdn.net/aninstein/article/details/108437847)中说明了Nginx的编译模块，即==nginx -V==输出的内容中，--with开头的部分模块即为Nginx的官方模块，其中的--with的模块有：
```linux
 --with-file-aio --with-ipv6 --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-http_auth_request_module --with-mail=dynamic --with-mail_ssl_module --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E'
```
 （1）==--with-http_slice_module==
主要是处理客户端状态，配置语法：
- Syntax：stub_status;
- Default： --
- Content：server， location 

配置方式：
```
location /lca {
    stub_status;
}
```

（2）==--with-http_random_index_module==
在主目录里面随机选择一个文件作为主页，一般场景是很少用到的。只是一般这个如果使用的话需要把index给注释掉。
- Syntax：random_index on|off;
- Default： random_index off;
- Content：server， location 

（3）==--with-http_sub_module==
服务端相应客户端的response的http内容的替换。场景：比如我们有很多Nginx服务端返回的结果，还需要统一的转换为另一种格式的数据内容的时候，不需要开发者再进行编码。可以是用这个模块的内容。类似response。

1. 用法1
- Syntax：sub_filter string replacement;   # string: 要替换的内容，replacement：要替换的内容
- Default： -- ;
- Content：http，server， location 

2.  用法2
- Syntax：sub_filter_last_modified on|off;  # 提示返回信息有没有发生更新，主要用于缓存的场景里，如果服务端发生了更新，则更新缓存。
- Default： sub_filter_last_modified off;
- Content：http，server， location 

3.  用法3
- Syntax：sub_filter_once on|off; 只是匹配第一个还是后面的都匹配;
- Default： sub_filter_once on;
- Content：http，server， location 

除了上述的几个配置之外，Nginx还有大量的内置模块配置，在Nginx官网上有详细配置的描述：http://nginx.org/en/docs/

### 3.2 Nginx的连接和请求的限制
- 连接频率的限制：limit_conn_module
- 请求频率的限制：limit_req_module

众所周是，HTTP是基于TCP的，因此需要进行TCP的三次握手完成连接。在HTTP2.0的版本中，HTTP对TCP连接已经能够实现多路复用，也就是所谓的长连接。因此：
 - 一次http请求一定是建立在一次tcp连接上
 - 一次tcp请求至少可以建立一次http请求，也可以建立多个http请求

所以，请求和连接的区别，即http请求和tcp连接。

#### 3.2.1 连接限制
（1）连接限制1
- Syntax：limit_conn_zone key zone=name:size;   # 用哪个空间作为key，zone的空间的名字，size即申请空间的大小
- Default： --
- Content：http


（2）连接限制2
- Syntax：limit_conn zone number;  # 结合先定义好的zone，与上面的zone=name是一个名字
- Default： --
- Content：http，server， location 


#### 3.2.1 请求限制
（1）连接限制1
- Syntax：limit_req_zone key zone=name:size rate=rate;   # 用哪个空间作为key，zone的空间的名字，size即申请空间的大小，rate速率
- Default： --
- Content：http


（2）连接限制2
- Syntax：limit_req zone number [burst=number\] [nodelay];  # 结合先定义好的zone，与上面的zone=name是一个名字
- 合先定义好的zone，与上面的zone=name是一个名字
- Default： --
- Content：http，server， location 