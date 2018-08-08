from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from BBS import create_app
from exts import db
from apps.cms import CMSUser,CMSRole,CMSpermission
from apps.front import models as front_models
from apps.models import BannerModel,BoardModel,PostModel

FrontUser = front_models.FrontUser
app = create_app()
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)
#命令行下添加管理人员
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功！')
@manager.command
def create_role():
    #1.访问者（修改个人信息）
    visitor = CMSRole(name='游客',desc='只能访问数据，不能修改')
    visitor.permissions = CMSpermission.VISITOR

    #2.运营角色（修改个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营',desc="管理帖子，管理评论，管理前台用户")
    operator.permissions = CMSpermission.POSTER | CMSpermission.VISITOR |\
                          CMSpermission.COMMENTER | CMSpermission.FRONTUSER | CMSpermission.BANNER
    #3.管理员（拥有绝大部分权限）
    admin = CMSRole(name='管理员',desc="拥有本系统所有权限")
    admin.permissions = CMSpermission.POSTER | CMSpermission.VISITOR |\
                        CMSpermission.COMMENTER | CMSpermission.FRONTUSER |\
                        CMSpermission.CMSUSER | CMSpermission.MODERATOR | CMSpermission.BANNER

    #4.开发者
    developer = CMSRole(name='开发者',desc='开发者专用')
    developer.permissions = CMSpermission.ALL_PERMISSION
    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

#给用户添加某个角色
@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功!')
    else:
        print('%s邮箱没有这个用户！'%email)

#添加前台用户
@manager.option('-t','-telephone',dest='telephone')
@manager.option('-u','-username',dest='username')
@manager.option('-p','-password',dest='password')
def create_frontUser(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()
    print('前台用户添加成功')


#测试一个用户是否拥有访问者权限
@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSpermission.VISITOR):
        print('这个用户有访问者权限')
    else:
        print('这个用户没有访问者权限')

#创建测试帖子
@manager.command
def create_test_post():
    for x in range(1,100):
        title = '标题%s' % x
        content = '内容%s'% x
        board = BoardModel.query.first()
        author = FrontUser.query.first()
        post = PostModel(title=title,content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print('测试帖子添加成功！')
if __name__ == '__main__':
    manager.run()