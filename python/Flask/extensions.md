# Extensions

> app.config 可以用来存储框架，扩展，程序本身的配置变量
> 还可以通过环境变量进行配置
> 使用所有扩展之前都需要初始化该扩展

## flask 依赖

### flask的两个主要依赖

1. Werkzeug(WSGI)
   > WSGI 将 HTTP 请求转换成 flask 程序能够处理的 Python 数据
   > WSGI 将应用程序的返回值转换成 HTTP 响应发送给 WEB 服务器
2. Jinja2(模板工具)

### 内置 web 服务器

> flask 内置了一个简单的开发服务器(由 Werkzeug 包提供)
> 安装 flask 后会添加一个 flask 命令(由 Click 包提供)
> flask run 启动开发服务器
> 通过@app.cli.command() 可以注册flask命令

### 安装flask会同时安装5个依赖包

- Jinja2
- MarkupSafe                           HTML字符转换工具
- Werkzeug
- Click                                命令行工具
- itsgangerous                         提供各种加密功能

## pipenv

> 虚拟环境包管理工具
> 安装 pipenv　后程序可识别　.flaskenv 文件(保存一般环境变量)

```shell
# 更新包
pipenv update package_name

# 初始化虚拟环境
pipenv install
> 目录下会生成 Pipfile 和 Pipefile.lock

# 将虚拟目录保存在当前目录下
export PIPENV_VENV_IN_PROJECT=1

# 设置敏感信息的环境变量(识别 .env 文件)
pip install python-dotenv
虚拟环境文件夹在(可以设置环境变量PIPENV_VENV_IN_PROJECT使虚拟环境文件夹保存在工作目录下)

# 激活虚拟环境(需要当前目录存在 Pipfile 文件)
pipenv shell

# 退出虚拟环境
exit

# 使用虚拟环境执行程序
pipenv run py *.py

# flask shell ipython 支持
pip install flask_shell_ipython
```

> flask run  debug_mode= off的问题, 命令行 export FLASK_DEBUG=1

## flask_script

> 使用flask_script使Flask应用可以接收命令行参数

```shell
# 打开python解释器
python app.py shell

# 运行web服务
python app.py shell runserver

# 设置启动shell时自动导入Flask实例，sqlalchemy实例以及模型等

def make_shell_context():
        return ditc(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",falske_script.shell(make_context=make_shell_context))
@manager.command
```

## flask-htttpauth(用户认证)
