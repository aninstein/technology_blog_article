## BGP学习

---
---

### 概念：
看这篇就可以：https://blog.csdn.net/le616616/article/details/121564799


## 1. BGP分类和区别
- EBGP：运行于不同AS之间的BGP称为EBGP，为了防止AS间产生环路，当BGP设备接收EBGP对等体发送的路由时，会将带有本地AS号的路由丢弃
- IBGP：运行于同一AS内部的BGP称为IBGP，为了防止AS内产生环路，BGP设备不将从IBGP对等体学到的路由通告给其他IBGP对等体，并与所有IBGP对等体建立全连接，为了解决IBGP对等体的连接数量太多的问题，BGP设计了路由反射器和BGP联盟
