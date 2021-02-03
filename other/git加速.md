# github clone加速
对于网上很多说的github进行clone非常慢，然后使用梯子进行加速。但是对于穷逼伸手党，有没有更快的办法呢？当然是有的，就是用以下的镜像服务器（好像只能够使用https进行clone了）：
```shell
# http的git加速：
# 如：
https://github.com/aninstein/xxx.git

# 加速：
https://github.com.cnpmjs.org/aninstein/xxx.git
```
即把==github.com==替换成==github.com.cnpmjs.org==

好像这样加速就只能够使用https加速了，那么第一次push的时候就需要输入github的用户名和密码，这个地方用以下命令进行永久保存用户名和密码：
```shell
git config --global credential.helper store
```

这个地方还有个坑，就是我们进行==git clone==的时候，因为使用的是==github.com.cnpmjs.org==的域名，因此在生成的.git/config是这样的：
```init
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[remote "origin"]
        url = https://github.com.cnpmjs.org/aninstein/xxx.git
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
        remote = origin
        merge = refs/heads/master
```

这时候直接进行==git push==代码有可能会报错，因此url需要改回==github.com==，我们一般提交代码也不会特别大，这时候速度慢一点也还可以接受了。