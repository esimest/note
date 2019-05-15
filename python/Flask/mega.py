"""
使用虚拟环境可以不干扰本机的python环境，且不开发过程中不需要管理员权限

render_template() #调用了jinja2模板引擎
使用模板的继承可以引用其他人已经设计好的页面，稍加修改变成自己的。还可以减少大量重复的工作.确保所有网页的一致性
在继承的block中，若要引用父模板的block中的内容，则需要添加super()，否则直接覆盖

使用flask_wtf实现表单
flask_wtf.FlaskForm  表单类
wtforms.StringField BooleanField...表单字段数据类型
wtforms.validators  表单验证函数
"""