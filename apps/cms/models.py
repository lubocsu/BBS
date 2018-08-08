from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

#权限
class CMSpermission(object):
    #通过二进制方式来表示 1111 1111
    #权限全开
    ALL_PERMISSION = 0b11111111
    #1.访问者权限
    VISITOR = 0b00000001
    #2.管理帖子权限
    POSTER = 0b00000010
    #轮播图权限
    BANNER = 0b00000011
    #3.管理评论的权限
    COMMENTER = 0b00000100
    #4.管理板块的权限
    MODERATOR = 0b00001000
    #5.管理前台用户权限
    FRONTUSER = 0b00010000
    #6.管理后台用户权限
    CMSUSER =   0b00100000
    #7.开发者
    ADMINER =   0b01000000

cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)


class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    permissions = db.Column(db.Integer,default=CMSpermission.VISITOR)
    users = db.relationship('CMSUser',secondary=cms_role_user,backref='roles')

class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)
    #重写构造函数，因为在命令行设置时只要password，没有_password
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    #在数据库中显示加密后的密码
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,rew_password):
        self._password=generate_password_hash(rew_password)

    def check_password(self,rew_password):
        result = check_password_hash(self._password,rew_password)
        return result

    #获取用户所有权限
    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    #判断用户是否具有相应的权限
    def has_permission(self,permission):
        all_permissions = self.permissions #直接调用上面permission还是获取用户拥有的权限
        result = all_permissions & permission == permission
        return result

    #判断用户是否是开发者
    @property
    def is_developer(self):
        return self.has_permission(CMSpermission.ALL_PERMISSION)
