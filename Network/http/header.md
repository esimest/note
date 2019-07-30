### HTTP Headers

- 通用首部（请求首部响应首部都可用）

- 请求首部
  - `proxy_set_header Host $host;`  指明了服务器的域名与端口，端口可选  
- 响应首部  

- 实体首部

- 扩展首部  (自定义消息首部以X-开头)
  - `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` X-Forwarded-For: 代理的ip + 之前的X-Forwarded-For
  - ` proxy_set_header X-Real-IP $remote_addr;` X-Real-IP: 客户端ip