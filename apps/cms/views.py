from flask import Blueprint,views,render_template,request,session,redirect,url_for,g
from .forms import (
    LoginForm,
    ResetpwdForm,
    ResetemailForm,
    AbannerForm,
    UbannerForm,
    AddBoardForm,
    UpdateBoardForm,
    DeleteBoardForm
)
from flask_paginate import Pagination,get_page_parameter
from .models import CMSUser,CMSpermission
from ..models import BannerModel,BoardModel,PostModel,HighlightPostModel
from .decorators import login_required,permission_required
from exts import db,mail
from tool import restful,zzcache
from flask_mail import Message #封装电子邮件消息
from tasks import send_mail
import config,string,random
bp = Blueprint("cms",__name__,url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')
#登录视图函数
class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)
    def post(self):
        # 表单验证
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    #如果设置了session.permanent =True
                    #过期时间为31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或者密码错误')
        else:
            message = form.get_error()
            return self.get(message=message)

#通过查询字符串方式获取用户所传的邮箱地址（/email_captcha/?email=xxx@qq.com）
@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数')
    #给用户输入的邮箱发送验证码
    source= list(string.hexdigits) #生成0-9 a-f A-F字符串且转换为列表
    captcha ="".join(random.sample(source,6))
    # message = Message("ZZ论坛邮箱验证码",recipients=[email],body="您的验证码是:%s"%captcha)
    #异常处理
    # try:
    #     mail.send(message)
    # except:
    #     return restful.server_error()
    try:
        send_mail.delay("ZZ论坛邮箱验证码",[email],"您的验证码是:%s"%captcha)
    except:
        return restful.server_error()

    #讲邮箱和验证码缓存到memcached中
    zzcache.set(email,captcha)
    return restful.success()

@bp.route('/email/')
def send_email():
    message = Message('测试邮件',recipients=['15111390080@163.com'],body='快点找工作了啦！！！')
    mail.send(message)
    return 'success'


#注销登录
@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))
#个人信息界面
@bp.route('/percenter/')
@login_required
def percenter():
    return render_template('cms/cms_percenter.html')
#更改密码
class Change_pwd(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_changepwd.html')
    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
              user.password = newpwd
              db.session.commit()
              return restful.success()
            else:
                return restful.params_error("旧密码错误")
        else:
            messagr = form.get_error()
            # print("+++++++++++")
            # print(messagr)
            # print("+++++++++++")

            return restful.params_error(messagr)
# 修改邮箱
class Resetemail(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/resetemail.html')
    def post(self):
        form = ResetemailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())

#帖子
@bp.route('/posts/')
@login_required
@permission_required(CMSpermission.POSTER)
def posts():
    # 帖子分页
    page = request.args.get(get_page_parameter(), type=int, default=1)  # 指定当前是第几页,默认显示第一页
    start = (page - 1) * config.PER_PAGE  # 每一页开始位置
    end = start + config.PER_PAGE  # 每一页结束位置
    posts_p = PostModel.query.order_by(PostModel.id.desc()).slice(start, end)
    total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0)
    context = {
        'posts': posts_p,
        'pagination':pagination
    }
    return render_template('cms/cms_posts.html',**context)

#移除帖子
@bp.route('/dposts/',methods=['POST'])
@login_required
@permission_required(CMSpermission.POSTER)
def dposts():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error(message='请传入帖子id!')
    # post = PostModel.query.filter_by(id=post_id).first()
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message='没有这篇帖子！')
    db.session.delete(post)
    db.session.commit()
    return restful.success()

@bp.route('/comments/')
@login_required
@permission_required(CMSpermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')

# 板块
@bp.route('/boards/')
@login_required
@permission_required(CMSpermission.MODERATOR)
def boards():
    board_moldes = BoardModel.query.all()
    context={
        'boards': board_moldes
    }
    return render_template('cms/cms_boards.html',**context)


@bp.route('/fusers/')
@login_required
@permission_required(CMSpermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_required
@permission_required(CMSpermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSpermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


#轮播图管理界面
@bp.route('/banners/')
@login_required
@permission_required(CMSpermission.BANNER)
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)


#添加轮播图
@bp.route('/abanner/',methods=['POST'])
@login_required
@permission_required(CMSpermission.BANNER)
def abanner():
    form = AbannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_b = form.image_b.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_b=image_b,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


#更新轮播图
@bp.route('/ubanner/',methods=['POST'])
@login_required
@permission_required(CMSpermission.BANNER)
def ubanner():
    form = UbannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_b = form.image_b.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner_id = form.banner_id.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_b = image_b
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个轮播图!")
    else:
        return restful.params_error(message=form.get_error())


#删除轮播图
@bp.route('/dbanner/',methods=['POST'])
@login_required
@permission_required(CMSpermission.BANNER)
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图Id!')
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()

# 添加板块
@bp.route('/aboard/',methods=['POST'])
@login_required
@permission_required(CMSpermission.MODERATOR)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())

#更新板块
@bp.route('/uboard/',methods=['POST'])
@login_required
@permission_required(CMSpermission.MODERATOR)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board_id = form.board_id.data
        board = BoardModel.query.filter_by(id=board_id).first()
        if board:
            # print(board.name)
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())


#删除板块
@bp.route('/dboard/',methods=['POST'])
@login_required
@permission_required(CMSpermission.MODERATOR)
def dboard():
    form = DeleteBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        board = BoardModel.query.filter_by(id=board_id).first()
        if board:
            db.session.delete(board)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块')
    else:
        return restful.params_error(message=form.get_error())

#帖子加精接口
@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSpermission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id!')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(('没有这篇帖子！'))
    highlight = HighlightPostModel(post_id=post_id)
    db.session.add(highlight)
    db.session.commit()
    return restful.success()

#帖子取消加精接口
@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSpermission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id!')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(('没有这篇帖子！'))

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


bp.add_url_rule('/changepwd/',view_func=Change_pwd.as_view('changepwd'))
bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetemail/',view_func=Resetemail.as_view('resetemail'))