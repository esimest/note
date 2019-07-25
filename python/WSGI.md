# WSGI (Python Web Server GateWay Interface)

> wsgi 是一个用于协调 web 应用与 web 服务器的接口。使得开发者使用特定的 web 框架使被绑定在特定的 web 服务器上
> wsgi 使得遵守这个协议的框架、应用 或 服务器/网管 可以间接沟通。
> 服务器遵守了 wsgi 协议，则可以与所有实现了 wsgi 接口的应用进行交互
> 应用实现了 wsgi 协议，则可以与所有实现了 wsgi 接口的服务器交互
> 实现一个 wsgi 中间件（同时实现两侧接口），则可以连接所有遵循 wsgi 的服务器和应用

## 应用侧

```python
HELLO_WORLD = b'Hello World !\n'

# 函数实现
def simple_app(environ, start_response):
    """"
    服务器调用         simple_app 传入 environ 和 start_response
    simple_app        处理后返回响应给服务器
    start_response    将响应头返回给服务器
    """
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    # 将响应体返回给服务器
    return [HELLO_WORLD]

# 类实现

class AppClass:
    def __init__(self, environ, start_response):
      self.environ = environ
      self.start = start_response

    def __call__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD
```

## 服务侧

```python
import os, sys

enc, esc = sys.getfilesystemencoding(), 'surrogateescape'

def unicode_to_wsgi(u):
    return u.encode(enc, esc).decode('iso-8859-1')

def wsgi_to_bytes(s):
    return s.encode('iso-8859-1')

def run_with_cgi(application):
    environ = {K : unicode_to_wsgi(v) fo k, v in os.environ.iterms()}
    environ['wsgi.input']        = sys.stdin.buffer
    environ['wsgi.erros']        = sys.stderr
    environ['wsgi.version']      = (1, 0)
    environ['wsgi.multithread']  = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once']     = True

    if environ.get('HTTPS', 'off') in ('on', 1):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        out = sys.stdout.buffer

        if not headers_set:
            raise AssertionError("write() before start_response()")
        elif not headers_sent:
            status, response_headers = headers_sent[:] = headers_set
            out.write(wsgi_to_bytes(f'Status: {status} \r\n'))
            for header in response_headers:
                out.write(wsgi_to_bytes(f'{header}: {header}\r\n'))
            out.write(wsgi_to_bytes('\r\n'))

        out.write(data)
        out.flush()

    def start_response(satus, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    raise exec_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None
        elif headers_set:
            raise AssertionError("Headers alredy set!")

        headers_set[:] = [status, response_headers]

        return write


    result = application(environ, start_response)
    try:
        for data in result:
            if data:
                write(data)
            if not headers_sent:
                write('')
    finally:
        if hasattr(result, 'close'):
            result.close()

```
