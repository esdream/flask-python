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

`app.route`修饰器中添加methods参数告诉Flask在映射中将这个视图函数注册为GET和POST请求的处理程序。默认只注册为GET请求。
```python
app.route('/', methods=['GET', 'POST'])
```

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

## 模板
---
### 渲染模板
---
Flask提供的`render_template`函数把Jinja2模板引擎集成到程序中。
`render_template`函数的第一个参数是模板的文件名，随后的参数都是键值对，表示模板变量中对应的真实值。

**注:模板中的语法应使用Jinja的语法格式而不是html的语法格式,例如注释应使用{# ... #}语法。**
```Jinja2
{# note: disabled template because we no longer use this
    {% for user in users %}
        ...
    {% endfor %}
#}
```

### 变量
---
Jinja2中可以使用 **过滤器** 修改变量。过滤名添加在变量名之后，中间用竖线分隔。

|过滤器名|说明|
|---|---|
|safe|渲染时值不转义|
|capitalize|首字母大写，其他小写|
|lower|转换成小写|
|upper|转换成大写|
|title|每个单词首字母大写|
|trim|把首位空格去掉|
|striptags|渲染之前把值中所有HTML标签去掉|
|||

**注：千万不要在不可信的值上使用safe过滤器，例如用户在表单中输入的文本。**

### 控制结构
---
Jinja2中支持条件控制、循环、宏等控制语句。

另一种重复使用代码的方式是模版继承。例如下方代码中`block`标签定义的元素可以在衍生模版中修改。
```jinja2
<html>
<head>
    {%block head%}
    <title>{%block title%}{%endblock%} - My Application</title>
    {%endblock%}
</head>
<body>
    {%block body%}
    {%endblock%}
</body>
</html>
```
在衍生模版中，修改`block`标签内定义的内容。`extends`指令声明模版继承自`base.html`。在`block head`模块中，由于模版中内容不是空的，所以用`super()`获得模版中的内容。如果不对模板中的某一`block`的内容进行修改，则不需要在子文件中写出。
```Jinja2
{%extends "base.html"%}
{%block title%}Index{%endblock%}
{%block head%}
    {{super()}}
    <style></style>
{%endblock%}
{%block body%}
<h1>Hello Dva</h1>
{%endblock%}
```

### 自定义错误页面
---
Flask允许程序使用基于模板的自定义错误页面，通过装饰器修饰。
```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
```
其中`404.html`和`500.html`可以自己定义。

### 链接
---
在编写多个路由的程序时，经常需要编写包含可变部分的动态路由。Flask提供了`url_for()`函数。可以使用程序URL中映射保存的信息生成URL。
```python
from flask import url_for
```
视图函数最简单的用法是以视图函数名作为参数，返回对应的URL。例如在`view.py`中有一个视图函数名称为`index`。则`url_for('index')`返回的结果是`/`。调用`url_for('index', _external=True)`将会返回绝对地址，例如在本地运行视图函数，则返回'http://localhost:5000'。
生成动态地址时，将动态部分作为关键字参数传入`url_for`即可；同时`url_for`的关键字参数不限于动态路由，函数能将任何额外参数传入查询字符串中，例如`url_for('index', page=2)`返回结果是`/?page=2`。

### 静态文件
---
Flask对静态文件的引用被当成一个特殊的路由，即`static/<filename>`。静态文件包括HTML代码中引用的图片、JavaScript源码和CSS。默认情况下，Flask会在程序根目录中名为`static`的子目录中寻找静态文件。

### 本地化日期和时间
---
服务器需要同一时间单位，通常使用UTC。而要在服务器使用UTC，在用户浏览器上使用当地时间，一种优雅的解决方案是 **把时间单位发送至浏览器转换成当地时间，然后渲染** 。`Flask-Moment`可以将实现这一功能的`moment.js`集成至Jinja2模版中。

## Web表单
---
### 跨站请求伪造保护
---
`app.config`字典可以用来存储框架、扩展和程序本身的配置变量。这个对象还提供了一些方法，可以从文件或环境中导入配置值。
为了实现表单免受跨站请求伪造（CSRF）的攻击，Flask需要通过`app.config`设置一个密钥，`Flask-WTF`通过这个密钥生成加密令牌，再用令牌验证请求中表单数据的真伪。

### 表单类
---
使用`Flask-WTF`时，每个Web表单都由一个继承自Form的类表示，这个类定义表单中的一组字段，每个字段用对象表示。字段对象可以添加一个或者多个验证函数，用来验证用户的输入值是否符合要求。
```python
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
```
其中`StringField`和`SubmitField`就是要定义的字段的类，使用时传入参数初始化成对象。`StringField`对应前端表单的属性为`type="text"`的`<input>`元素，`SubmitField`对应前端表单属性为`type="submit"`的`<input>`元素。
`Required`是验证函数的一种，使用时传入字段对象的`validators`参数中。
这时候后端对象创建好了，要在模版中将表单渲染成HTML。在`template/index.html`中使用`Flask-Bootstrap`渲染表单。
```Jinja2
{%extends "base.html"%}
{%import "bootstrap/wtf.html" as wtf%}

{%block title%}Flasky{%endblock%}

{%block page_content%}
<div class="page-header">
    <h1>Hello, {%if name%}{{name}}{%else%}Stranger{%endif%}</h1>
</div>
{{wtf.quick_form(form)}}
{%endblock%}
```

最后在视图函数中，还要定义处理表单的路由方法。
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if(form.validate_on_submit):
        name = form.name.data
        form.name.data = ''
        print(name)
    return render_template('index.html', form=form, name=name)
```
视图函数中创建一个`NameForm`类的实例表示表单。如果验证函数通过，`validate_on_submit()`方法返回True。

### 重定向和用户会话
---
在表单中，最好不要让Web程序把POST请求作为浏览器发送的最后一个请求。最好的方法是，使用 **重定向** 作为POST请求的响应，响应内容是URL。浏览器收到这种相应时，会向重定向的URL发送GET请求，显示页面内容。
由于重定向会丢失之前POST请求的`form.name.data`数据，可以将数据存储在用户会话中。这是请求上下文中的变量，名为`session`。

### Flash消息
---
请求完成后，有时需要让用户知道状态发生了变化，这里可以使用确认消息、警告或者错误提醒。使用`flash()`函数可以实现这种效果。

仅调用`flash()`函数不能把消息显示出来，程序使用的模板要渲染这些信息。最好在 **基模板** 中渲染Flash信息。

## 数据库
---
### Flask-SQLAlchemy
---
在Flask-SQLAlchemy中，数据库使用URL指定。

|数据库引擎|URL|
|---|---|
|MySQL|mysql://username:password@hostname/database|
|Postgres|postgresql://username:password@hostname/database|
|SQLite(Unix)|sqlite:////absolute/path/to/database|
|SQLite(Windows)|sqlite:///c:/absolute/path/to/database|
|||

在这些URL中，`hostname`表示MySQL服务所在的主机，可以是本地主机，也可以是远程服务器。数据库服务器上可以托管多个数据库，因此`database`表示要使用的数据库名。SQLite数据库不需要使用服务器。

程序使用的数据库URL必须保存到Flask配置对象的 **SQLALCHEMY_DATABASE_URI** 键中。另外 **SQLALCHEMY_COMMIT_ON_TEARDOWN** 键设置为`True`时，每次请求结束后会自动提交数据库中的变动。

### 定义模型
---
模型表示程序使用的持久化实体，在ORM中，模型一般是一个Python类，类中的属性对应数据库表中的列。

Flask-SQLAlchemy创建的数据库实例为模型提供了一个基类以及一系列辅助类和辅助函数，可用于定义模型的结构。定义如下：
```python
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ == 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username
```
其中`__tablename__`定义在数据库中使用的表名，如果没有定义，Flask-SQLAlchemy会使用一个默认名字。其余的类变量都是该模型的属性，被定义为`db.Column`类的实例。

常用的SQLAlchemy列类型

|类型名|Python类型|说明|
|---|---|---|
|Integer|int|普通整数，32位|
|SmallInteger|int|取值范围小的整数，16位|
|BigInteger|int或long|不限制精度的整数|
|Float|float|浮点数|
|Numeric|decimal|定点数|
|String|str|变长字符串|
|Text|str|变长字符串，对较长或不限长度的字符串做了优化|
|Unicode|unicode|变长Unicode编码串|
|Boolean|bool|布尔值|
|Date|datetime.date|日期|
|Time|datetime.time|时间|
|Interval|datetime.timedelta|时间间隔|
|Enum|str|一组字符串|
|PickleType|任何python对象|自动使用Pickle序列化|
|LargeBinary|str|二进制文件|
||||

常用的SQLAlchemy列选项

|选项名|说明|
|---|---|
|primary_key|为True时这列就是表主键|
|unique|为True时这列不允许重复值|
|index|为True时为该列创建索引|
|nullable|为True时允许出现空值|
|default|为这列定义默认值|
|||