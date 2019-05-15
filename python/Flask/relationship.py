#一对多 == 多对一

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):   #   多
    id = db.Column(db.Integer)
    title = db.Column(db.String())
    text = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#声明外键


class User(db.Model): #   一
    id = db.Column(db.String())
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(    #声明映射关系。一般在一对多的一一侧声明
        'Post',
        backref = 'user',
        lazy = 'dynamic'
    )
    
# 多对多
# 多对多关系处理的方式是，在两个表之间添加一个关联表
# 从而变成 一对多对一
"""
学生和课程之间是多对多关系。可以添加一个选课表，使其形成 一对多对一
"""
#db.Table()有sqlalchemy管理
registrations = db.Table('registrations',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    classes = db.relationship('Class',
        secondary=registrations,
        backref=db.backref('students', lazy='dynamic'),
        lazy='dynamic')
class Class(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

# 自引用
#关注者和被关注者之间存在的就是自引用关系
#通过 关注 连接起来
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'), 
        primary_key=True)
    followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True)
    timestamp = db.Column(db.Datetime, default=datetime.utcnow)

class User(db.Model):
    followed = db.relationship('Follow',
                                foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                 foreign_keys=[Follow.followed_id],
                                 backref=db.backref('followed', lazy='joined'),
                                 lazy='dynamic',
                                 cascade='all, delete-orphan')