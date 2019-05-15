"""

全局变量
current_app, request, session, g
四个对象都是真实对象的代理(proxy), 若要获取真是对象可以通过对代理对象调用_get_current_object()获取
app = Flask(__name__)
flask.request
request 对象
request.path/full_path/host/full_host
常用的request对象的属性和方法
args blueprint cookies data endpoint files form values
get_data(cache=True, as_text=False, parse_from_data=False)
get_json(self, force=False, silent-Flask, cache=True)
headers is_json json method referrer sechme user_agent


app.url_map 保存了URL和视图函数的映射关系  flask routes显示映射关系

URL变量转换器 表2-6  <转换器: 变量名>
string int float path any uuid

请求钩子(Hook) 一般使用装饰器实现，使我们可以对请求进行预处理或后处理，如验证登陆等
表2-7
Flask默认实现的五种请求钩子
before_first_request
before_request
after_request
teardown_request :注册一个函数，即使处理请求过程中有未处理的异常，请求结束后也将执行这个函数
after_this_request
上下文钩子
teardown_appcontext

状态吗 表2-9
使用redirect()时，默认状态码为302可以使用code关键字参数改变状态码
redirect(url_for(视图函数名))
flask的错误响应处理由werkzeug.exceptions提供
abort(404）手动返回错误

响应对象 Reponse
视图函数可以返回最多由三个元素组成的元组：响应体 状态码  首部字段(dict)
可以通过调用make_reponse()直接生成响应对象
默认情况下 我们只返回响应主体，其他交由服务器解决

Flask中的默认响应格式(MIME类型)为 Content-Type: text/html(类型名/子类型名(文件扩展名)); charset=utf-8
可以通过显示的reponse.mimtype = 'application/json'来修改mime类型
或 reponse.headers['Content-Type']='text/html; charset=utf-8'
html用于展示数据，xml用于定义数据
xml: 重用性高，体积大，处理和解析熟读慢
json: 轻量，简洁，容易阅读和解析，和javascript更兼容
jsonify()

Cookie
通过respone.set_cookie()来设置cookie  表2-11
通过request.cookies.get()来获取对应名称的cookie值，由于cookie是明文的所以很危险
Flask 中的session 是用来加密Cookie的，默认情况下将其存储在名为session的cookie中
通过设置 Flask.secret_key 或 app.config['SECRET_KEY'] 来设置加密数据的密钥

获取上一个页面的RUL
(1) 通过 request.referrer
(2) 在上一个页面发送请求是添加一个参数表明当前URL，通过这个参数获取上一个页面的RUL


防范SQL注入攻击的几种方式
1) 使用ORM，能起到一定效果
2) 验证输入类型，与视图函数接收变量的数据类型保持一致
3) 参数化查询

XSS(跨站脚本攻击)

CSRF(跨站请求伪造)
"""