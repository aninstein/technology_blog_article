# django从1.11升级到4.0.4，同时升级了python2到python3

---
---

1. python3的django取消了ugettext_lazy
```python
from django.utils.translation import gettext_lazy as _  # python3

from django.utils.translation import ugettext_lazy as _  # python2
```

2. django的model的on_delete字段变成了必填



3. django 3.0之后url变更为re_path

https://docs.djangoproject.com/pl/4.0/releases/4.0/#features-removed-in-4-0

```python
from django.urls.conf import url  # python2, django < 3.0

from django.urls import re_path  # python3, django >= 3.0
```

4.  admin的url集合不需要include就能使用

```python
re_path(r'^index/', include(admin.site.urls))  # python2

re_path(r'^index/', admin.site.urls)  # python3
```

5. reder方法更新

https://www.jianshu.com/p/f9455da2fc97

```python
from django.shortcuts import render_to_response  # python2

from django.shortcuts import render  # python3
```

6. 中间件的参数变化：

settings.py
```python
MIDDLEWARE_CLASS = []  # python2

MIDDLEWARE = []  # python3
```


7. 中间件需要继承MiddlewareMixin

通过看源码可以看到

site-packages\django\core\handlers\base.py, lineon: 61

```python
mw_instance = middleware(adapted_handler)
```

而原先的没有传入参数，因此继承自MiddlewareMixin，例如：
```
class BlockedIpMiddleware(object):  # python2


class BlockedIpMiddleware(MiddlewareMixin):  # python2
```

在settings.py文件中
```python
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'revision.middleware.BlockedIpMiddleware',
]
```

8. python3需要添加autoid的字段

```
# python3 module auto id, https://www.liujiangblog.com/blog/63/
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
```

9. 有可能数据显示为object(数字)的问题，需要改一下model类，添加__str__方法，返回需要显示的字段，即原先__unicode__方法返回的内容

```
    def __str__(self):
        return self.name
```

10. python3的encode方法是返回的byte格式字符，不能与str类型进行字符串相加操作

```
"aninstein".encode("utf-8") + "niubi"  # python2

str("lichangan".encode("utf-8")) + "niubi"  # python3

或者
"aninstein" + "nuibi"  # python3完全不需要使用encode
```