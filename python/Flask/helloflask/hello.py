"""
pipenv 可以自动识别.flaskenv 但是要识别.env需要安装python-dotenv
flask run  debug_mode= off的问题
命令行 export FLASK_DEBUG=1

flask shell 运行ipython 需要安装flask_shell_ipython
"""
"""
flask的两个主要依赖
1. Werkzeug(WSGI),WSGI将HTTP请求转换成FLASK程序能够处理的Python数据
WSGI将应用程序的返回值转换成HTTP响应发送给WEB服务器
2. Jinja2(模板工具)

安装flask会同时安装5个依赖包
Jinja2
MarkupSafe  HTML字符转换工具
Werkzeug
Click   命令行工具
itsgangerous   提供各种加密功能
"""
"""
PyPI中的包名称不区分大小写
pipenv集成了virtual
pip install pipenv

pipenv update package_name (更新)
pipenv install(初始化虚拟环境) (export PIPENV_VENV_IN_PROJECT=1可以将虚拟目录保存在当前目录下)
(使用python-dotenv管理flask环境变量).env设置敏感信息的环境变量，.flaskenv设置flask相关的环境变量
虚拟环境文件夹在(可以设置环境变量PIPENV_VENV_IN_PROJECT使虚拟环境文件夹保存在工作目录下)
C:\Users\Administrator\.virtualenvs\
~/.local/share/virtualenvs/
当前目录只有Pipfile(取代了不易管理的requirements.txt) 和Pipfile.lock

pipenv shell 激活虚拟环境(需要当前目录存在Pipfile文件)
exit 退出虚拟环境
pipenv run py *.py
"""

"""
Flask类表示一个Flask程序
app = Flask(__name__)  # 创建了一个flask程序的实例

在一个Web 应用里，客户端和服务器上的Flask 程序的交互可以简单概括为以下几步：
1) 用户在浏览器输入URL访问某个资源。
2) Flask 接收用户请求并分析请求的URL。
3) 为这个URL找到对应的处理函数。
4) 执行函数并生成响应，返回给浏览器。
5) 浏览器接收并解析响应，将信息显示在页面中。

flask 内置了一个简单的开发服务器(由Werkzeug包提供)
安装flask后会添加一个flask命令(由Click包提供)
flask run 启动开发服务器
通过@app.cli.command() 可以注册flask命令
"""
