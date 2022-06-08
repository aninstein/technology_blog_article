# django admin
---
---

## 1. 用python web的一些建议


对比一下常见的几种web框架的使用场景：
### Django
- Django走的大而全的方向，开发效率高。它的MTV框架，自带的ORM,admin后台管理,自带的sqlite数据库和开发测试用的服务器，给开发者提高了超高的开发效率。
- 重量级web框架，功能齐全，提供一站式解决的思路，能让开发者不用在选择上花费大量时间。
- 自带ORM和模板引擎，支持jinja等非官方模板引擎。
- 自带ORM使Django和关系型数据库耦合度高，如果要使用非关系型数据库，需要使用第三方库
- 自带数据库管理app

使用建议：上述的优点让Django虽然比较完全，但是因为不需要开发者去选择，反而限制了开发者，现在来看使用django的主要是看中了django-admin能够快速构建一个后台管理的环境。

### Flask

- Flask是轻量级的框架，自由、灵活、可扩展性强，核心基于Werkzeug WSGI工具和jinja2模板引擎。
- 适用于做小网站以及web服务的API,开发大型网站无压力，但架构需要自己设计
- 与关系型数据库的结合不弱于Django，而与非关系型数据库的结合远远优于Django

使用建议：比较合适拓展，效率也还可以，把一些组件给第三方去使用，形成了flask生态。合适有能力自己做设计的，相对复杂的网站。

### Tornado

- Tornado走的是少而精的方向，性能优越，它最出名的异步非阻塞的设计方式。
- Tornado的两大核心模块：
	- iostraem:对非阻塞的socket进行简单的封装
	 - ioloop:对I/O多路复用的封装,它实现一个单例

使用建议：tornado使用的epoll，异步非阻塞的方式编写代码会比较难一些，而且真正的高并发项目一般也不用python写了，所以很少人使用tornado了。


### fastapi

- 快速：可与 NodeJS 和 Go 比肩的极高性能（归功于 Starlette 和 Pydantic）
- 高效编码：提高功能开发速度约 200％ 至 300％
- 更少 bug：减少约 40％ 的人为（开发者）导致错误。
- 智能：极佳的编辑器支持。处处皆可自动补全，减少调试时间
- 简单：设计的易于使用和学习，阅读文档的时间更短
- 简短：使代码重复最小化。通过不同的参数声明实现丰富功能。bug 更少
- 健壮：生产可用级别的代码。还有自动生成的交互式文档
- 标准化：基于（并完全兼容）API 的相关开放标准：OpenAPI (以前被称为 Swagger) 和 JSON Schema。

使用建议：python web新秀，比Tornado还快，说是能比得上go，但是生态还不完善。建议用在需求比较小的，只有api请求和响应的服务（类似GRPC）的服务，大型的网站目前因为生态不完善可能比较痛苦。

### 如何选择框架/自研
- 明确业务。明确自己做的是什么，如只是一个后台关系系统，那选择django-admin是否就能够满足要求
- 充分调研。充分了解和调研技术内容，查看官方文档学习，并且了解框架的最优解决方案和使用场景
- 提前避坑。框架总是有好有坏，则缺点的部分是否是重要的
- 前瞻性。自研的代码并不是越少越好，如果是一个成长性的产品，充分讨论设计再选型很有必要
	- 是否有会持续更新需求
	- 是否有大量定制需求
	- 是否有联动需求
	- 学习成本
	- 研发成本

### web开发的规范化

- 规范化总是好的，但是合适自身业务的规范化才是最好的
- flask的规范化更多靠的是开发者，这个就很看重开发者的水平。django的规范化更多靠的是框架，主要是从学习框架中学习规范。


## 2. django admin

先了解django的内置组件
- Admin是对model中对应的数据表进行增删改查提供的组件
- model组件：负责操作数据库
- form组件：1.生成HTML代码2.数据有效性校验3校验信息返回并展示
- ModelForm组件即用于数据库操作,也可用于用户请求的验证

可以使用命令直接构建：
```
python manage.py createsuperuser
```

### 2.1 数据库生成
参考：https://blog.csdn.net/u012867040/article/details/103028784/

manage.py脚本使用
manage.py是每个django项目中自动生成的一个用于管理项目的脚本文件。需要通过python命令执行。manage.py接受的是Django提供的内置命令。

执行方式：
```
python manage.py 内置命令
```

内置命令包含：
- makemigrations：创建更改文件（数据库）
- migrate：将生成的py文件应用到数据库（数据库）
- inspectdb：反向生成models文件
- runserver：运行服务器：默认端口为8000，默认localhost为127.0.0.1
- startapp appname：新建App
- startproject projectname ：新建Django project

我们在==models.py==中写了model类之后，可以通过migrate应用到数据库：
```
python manage.py makemigrations
python manage.py migrate
```

### 2.2 数据库操作
django的数据库操作主要就是ORM。但是在django的admin中，封装的更加彻底，只需要admin.ModelAdmin中进行编排，并不需要自己写增删改查的代码。

### 2.3 页面规划
#### 2.3.1 admin路由
admin路由：admin.site.urls
配置方法：
```
# urls.py
from django.conf.urls import url
from django.contrib import admin
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
```

### 2.3.2 admin.ModelAdmin
可以理解为，这个是admin的一个页面的编排工具

- 参考官网：https://docs.djangoproject.com/zh-hans/4.0/ref/contrib/admin/
- 参考博客：https://www.cnblogs.com/feifeifeisir/p/12870181.html

ModelAdmin一些常用的字段：
- list_display: 显示页面有哪些字段可以进行配置
- filter_horizontal: 多对多的情况下，进行拖拽
- ordering: 列表页面根据什么进行排序
- search_fields: 支持搜索的字段
- list_filter：设置来激活管理更改列表页面右侧侧栏的过滤器
- readonly_fields：只读字段
- save_as：设置 save_as，在管理更改表格时启用 “另存为新” 功能。通常情况下，对象有三个保存选项。“保存”、“保存并继续编辑” 和 “保存并添加另一个”。如果 save_as 为 True，则 “保存并添加另一个” 将被 “另存为新” 按钮所取代，该按钮将创建一个新的对象（具有新的 ID），而不是更新现有的对象。默认情况下，save_as 被设置为 False。

ModelAdmin一些常用方法：
- ==ModelAdmin.save_model()==：save_model 方法被赋予 HttpRequest、一个模型实例、一个 ModelForm 实例和一个基于是否添加或更改对象的布尔值。覆盖这个方法可以进行保存前或保存后的操作。调用 super().save_model() 使用 Model.save() 保存对象。
- ModelAdmin.get_ordering()：get_ordering 方法以 request 为参数，并期望返回一个类似于 ordering 属性的 list 或 tuple 的排序。例如：
- ==ModelAdmin.get_readonly_fields()==：get_readonly_fields 方法是给定 HttpRequest 和被编辑的 obj（或者在添加表单中给定 None），并期望返回一个 list 或 tuple 的字段名，这些字段名将被显示为只读，如上面 ModelAdmin.readonly_fields 部分所述。
- ==ModelAdmin.get_urls()==：ModelAdmin 上的 get_urls 方法以与 URLconf 相同的方式返回用于该 ModelAdmin 的 URL。 因此，你可以按照 URL调度器 中的文档来扩展它们
- ==ModelAdmin.get_form(request, obj=None, **kwargs)==：返回一个 ModelForm 类，用于管理员添加和更改视图，参见 add_view() 和 change_view()。
基本实现使用 modelform_factory() 来子类 form，通过 fields 和 exclude 等属性进行修改。所以，例如，如果你想为超级用户提供额外的字段，你可以像这样换一个不同的基本表单
-  ==ModelAdmin.has_add/change/delete/module_permission(request)==：对对象的读写权限
-  ==ModelAdmin.get_queryset(request)==：ModelAdmin 上的 get_queryset 方法返回一个 QuerySet 的所有模型实例，这些实例可以被管理网站编辑。覆盖该方法的一个用例是显示登录用户拥有的对象


### 2.3.3 注册
需要把ModelAdmin和Model类，注册到admin上，如：
```python
admin.site.register(RevisionPost, RevisionPostAdmin)
```
这个admin.site的功能，可以参考：
- 官网：https://docs.djangoproject.com/zh-hans/4.0/ref/contrib/admin/#django.contrib.admin.AdminSite

### 2.4 参数校验
参数校验需要用到Forms的类内容，但是在使用ModelAdmin方法中有以下的变量：
```
ModelAdmin.form
```
如果不进行配置，则Form会自己生成一个from表单校验器==FormSet==，可以查看源码：
```python
        if request.method == 'POST' and cl.list_editable and '_save' in request.POST:
            FormSet = self.get_changelist_formset(request)
            formset = cl.formset = FormSet(request.POST, request.FILES, queryset=self.get_queryset(request))
            if formset.is_valid():
                changecount = 0
                for form in formset.forms:
                    if form.has_changed():
                        obj = self.save_form(request, form, change=True)
                        self.save_model(request, obj, form, change=True)
                        self.save_related(request, form, formsets=[], change=True)
                        change_msg = self.construct_change_message(request, form, None)
                        self.log_change(request, obj, change_msg)
                        changecount += 1

                if changecount:
                    if changecount == 1:
                        name = force_text(opts.verbose_name)
                    else:
                        name = force_text(opts.verbose_name_plural)
                    msg = ungettext(
                        "%(count)s %(name)s was changed successfully.",
                        "%(count)s %(name)s were changed successfully.",
                        changecount
                    ) % {
                        'count': changecount,
                        'name': name,
                        'obj': force_text(obj),
                    }
                    self.message_user(request, msg, messages.SUCCESS)

                return HttpResponseRedirect(request.get_full_path())
```

当然我们就可以重写这个校验器，如：
```python
class EmpForm(forms.Form):
    name = forms.CharField(min_length=4, label="姓名", error_messages={"min_length": "你太短了", "required": "该字段不能为空!"})
    age = forms.IntegerField(label="年龄")
    salary = forms.DecimalField(label="工资")
```

在admin中完成绑定：
```python
class EmpAdmin(admin.ModelAdmin):
	form = EmpForm
```


而Form类可以参考：
- 菜鸟：https://www.runoob.com/django/django-form-component.html
- 官网：https://docs.djangoproject.com/zh-hans/4.0/topics/forms/formsets/
- 博客：https://blog.csdn.net/m0_38109046/article/details/83186165


全文参考：
- [Django Admin管理后台详解(上)](https://zhuanlan.zhihu.com/p/47962034)
- [Django 管理站点](https://docs.djangoproject.com/zh-hans/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin)