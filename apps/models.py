from exts import db
from datetime import datetime

# 轮播图模型
class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    image_b = db.Column(db.String(255),nullable=False)
    link_url = db.Column(db.String(255),nullable=False)
    priority = db.Column(db.Integer,default=0)
    creat_time = db.Column(db.DateTime,default=datetime.now)


# 板块模型
class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)


# 帖子模型
class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text,nullable=False)
    board_id = db.Column(db.Integer,db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100),db.ForeignKey('frontuser.id'),nullable=False)
    praise_count = db.Column(db.Integer,default=0)
    create_time = db.Column(db.DateTime,default=datetime.now)
    board = db.relationship("BoardModel",backref="posts")
    author = db.relationship("FrontUser",backref="posts")


#加精模型
class HighlightPostModel(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    post = db.relationship("PostModel",backref='highlight')
    create_time = db.Column(db.DateTime, default=datetime.now)


#评论模型
class CommentModel(db.Model):
    __tablename__= 'comemnt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('frontuser.id'), nullable=False)
    author = db.relationship("FrontUser", backref="comments")
    post = db.relationship("PostModel",backref="comments")


# 点赞模型
class PraiseModel(db.Model):
    __tablename__= 'praise'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    fuser_id = db.Column(db.String(100),db.ForeignKey('frontuser.id'))
    post = db.relationship("PostModel", backref="praises")
    fuser = db.relationship("FrontUser",backref="praises")