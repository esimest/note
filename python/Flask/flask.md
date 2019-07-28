# flask 笔记

## 请求上下文

> Flask在请求分发之前 激活程序和请求上下文。处理结束后(返回响应)删除

```python
#获取上下文
app_ctx=app.app_context()

# 推送（激活）上下文。之后就可以使用上下文变量
app_ctx.push()
```

## 全局变量

> 当 app 读入配置并启动时 current_app, g 两个上下文变量就生效了，程序结束后失效
> 当一个请求被处理时，request, session 两个上下文就生效了，返回响应后失效

## 请求钩子

> 请求钩子。注册一个函数使其在特定时间起作用

- before_first_request
- before_request
- after_request
- teardown_request （即使有未处理的异常抛出，每次请求处后也要执行）

## Response

- redirect(url)                        生成重定向响应
- abort(status_code)                   生成错误响应
- url_for()                            重新生成一个url
- render_template                      获取url指定的模板
- url_for(view_function,arguemnts)
- url_for('static',filename = )
- app.errorhandler(404/403/500...)

## Factory Function

> 正常情况下 Flask 程序实例在运行主程序的同时创建
> 把创建实例的过程迁移至可显式调用的工厂函数中，可自决定创建实例的时间

## blueprint

> 蓝本中的路由处于休眠状态，直到被Flask注册后，才真正成为程序的一部分
