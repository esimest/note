#  wtforms 支持在python使用类定义表单

"""
模拟接受请求
>>> from flask import Flask
>>> app = Flask(__name__)
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> req_ctx = app.test_request_context()
>>> req_ctx.push()
>>> form = LoginForm()
>>> form.username()
'<input id="username" name="username" required type="text" value="">'

表单数据的验证是Web表单中一个很重要的主题

UUID 通用唯一识别码 唯一标识

使用Flask-CKEditor集成富文本编辑器

ORM实现的三层映射关系
表 Python类
字段  类属性 类属性 类属性
记录  类实例
"""