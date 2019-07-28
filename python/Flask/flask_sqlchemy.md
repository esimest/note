# flask_sqlalchemy

> flask 通过 flask_sqlalchemy 将关系型数据库数据库对象映射成 python 类
> 并通过方法对表数据进行 CRUD 操作

```shell
# 安装
pip install mysqlclient
pip install flask_sqlalchemy
```

## 初始化

```python
from flask import Flask
from flask_sqlchemy import SQLAlchemy
SQALCHEMY_DATABASE_URI = 'mysql://mysql:mysql@host:port/database'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=SQALCHEMY_DATABASE_URI

# 注册
db = SQLAlchemy(app)

# or
db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

"""
如果没有定义__init__方法，SQLAlchemy会自己定义一个接收所有
关键字参数的初始化方法。如果自己定义__init__,则必须自己显示的
声明所有关键字参数，或调用：
super(class_name,self).__init__(**kwargs)
"""
```

## CRUD

```python
#insert
user = User(username='username')
db.session.add(user) or db.session.add_all(list_of_users)
db.session.commit()

#query Model.query == db.session.query(Model)
users = User.query.all()
user = User.query.first()
users = User.query.limit(m,n).all()

#返回包含一页数据的对象
page = User.query.paginate(页数, 每页数量)

#当前页数
page.page

#总页数
page.pages

#当前页包含的数据
page.items

# 判断
page.has_prev
page.has_next

# 获取
page.prev()
page.next()

##条件查询
users = User.query.filter_by(username='????').all()/.first()
users = User.query.orderby(User.username.desc())

# from sqlalchemy.sql.expression import not_, or_

user = User.query.filter(User.username in_ [...])

# 删除
db.session.delete(...)
```
