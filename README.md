# flask-python

![python](https://img.shields.io/badge/python-3.5%2C3.6-blue.svg)

学习Flask的代码
---

## 配置与安装
---
### 使用conda environment
---
由于使用了Anoconda作为Python运行环境，所以创建虚拟环境使用了`conda env`
```shell
# 创建
$ conda create --name venv

# 启动
$ activate venv

# 关闭
$ deactivate
```

### 安装Flask
---
在`venv`环境下，运行
```shell
$ pip install flask
```

## 程序的基本结构
---
### Flask上下文
---
Flask为了避免大量参数把视图函数弄得一团糟，使用 **上下文** 临时把某些对象变为全局访问。
Flask中有两种上下文：**程序上下文** 和 **请求上下文**。Flask在分发请求之前激活/推送程序和请求上下文，请求处理完成后再将其删除，原理与Python中`with`引导的上下文作用类似（临时打开文件，处理完成后关闭）。

### 请求调度
---
程序收到客户端发来的请求时，要找到处理该请求的视图函数，Flask会在程序的 **URL映射** 中查找请求的URL。Flask使用 **app.route修饰器** 或 **非修饰器形式的app.add_url_rule()** 生成映射。

要查看Flask中的URL映射，使用`app.url_map`
```shell
$ from flask_structrue import app
$ app.url_map
Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
 <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
 <Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>,
 <Rule '/num/<id>' (HEAD, OPTIONS, GET) -> num>])
```

### 请求钩子
---
有时需要在处理请求之前或之后执行代码，例如在请求开始时，我们需要创建数据库链接或者认证发起请求的用户。Flask提供注册通用函数的功能，可以在请求分发到视图函数之前或之后调用。
请求钩子使用 **修饰器** 实现。Flask支持以下四种钩子：
    + before_first_request: 处理第一个请求之前运行
    + before_request: 每次请求之前运行
    + after_request: 如果没有异常抛出，在每次请求之后运行
    + teardown_request: 即使有异常抛出，也在每次请求之后运行

在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量`g`。

### 响应
---
Flask视图函数可以返回·`Response`对象。可以用`redirect`重定向，可以用`abort`处理错误。abort函数不会把控制权交还给调用它的函数，而是抛出异常把控制权交给Web服务器。

## Flask扩展
---
### 使用Flask-Script支持命令行选项
---
安装Flask-Script
```shell
$ pip install flask-script
```
在Flask程序`flask_structrue.py`中添加命令行解析功能。
```python
from flask.ext.script import Manager
app = Flask(__name__)
manager = Manager(app)

# ...

if(__name__ == '__main__'):
    manager.run()
```

然后执行
```shell
$ python flask_structrue.py
```
可以看到一组基本命令行选项。可以调试和启动命令行信息。
例如，下面的命令行告诉Web服务器在哪个网络接口上监听来自客户端的链接
```shell
$ python flask_structrue.py runserver --host 0.0.0.0
```
