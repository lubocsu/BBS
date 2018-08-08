from flask import Blueprint,views,render_template,request,url_for,session,g,redirect,abort
from .forms import SignupForm,SigninForm,AddPostForm,AddCommentForm,PraiseForm,CancelPraiseForm
from tool import restful,safetool
from .models import FrontUser
from ..models import BannerModel,BoardModel,PostModel,CommentModel,HighlightPostModel,PraiseModel
from exts import db
from .decorators import login_required
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy.sql import func

import config

bp = Blueprint("front",__name__)

@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int,default=None)#从前端拿到模版id
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(3)
    boards = BoardModel.query.all()
    sort = request.args.get("st",type=int,default=1)
    page = request.args.get(get_page_parameter(),type=int,default=1)#指定当前是第几页,默认显示第一页
    start = (page-1)*config.PER_PAGE #每一页开始位置
    end = start+config.PER_PAGE #每一页结束位置
    posts = None
    total = 0
    # 排序方式
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        #按照加精的时间倒序排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).\
            order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    elif sort == 3:
        #按照点赞数量排序
        query_obj = PostModel.query.order_by(PostModel.praise_count.desc())
    elif sort == 4:
        #按照评论数量排序
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).\
            order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())


    if board_id: #如果有则显示相应模版下的帖子
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    else:
        posts = query_obj.order_by(PostModel.id.desc()).slice(start,end)
        total = query_obj.count()
    pagination = Pagination( bs_version=3,page=page,total=total,outer_window=0)
    context ={
        'banners':banners,
        'boards':boards,
        'posts':posts,
        'pagination':pagination,
        'current_board':board_id,
        'current_sort':sort
    }
    # print('+++++++++++++')
    # print(type(banners))
    # print('+++++++++++++')
    return render_template('front/front_index.html',**context)

#发布帖子接口
@bp.route('/apost/',methods=['GET','POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html',boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
               return restful.params_error(message='没有这个板块！')
            post = PostModel(title=title,content=content,board_id=board_id)
            post.author = g.Front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())

#注销登录
@bp.route('/logout/')
@login_required
def logout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('front.signin'))


#帖子详情视图
@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if config.FRONT_USER_ID in session:
        fuser_id = g.Front_user.id
        praise = PraiseModel.query.filter_by(fuser_id=fuser_id).first()
        context = {
            'post': post,
            'praise': praise
        }
        return render_template('front/front_pdatail.html', **context)
    else:
        if not post:
            abort(404)
        context={
            'post': post
        }
        return render_template('front/front_pdatail.html',**context)


#添加评论
@bp.route('/acomment/',methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        post_id = form.post_id.data
        content = form.content.data
        post = PostModel.query.filter_by(id=post_id)
        if post:
            comment = CommentModel(content=content,post_id=post_id)
            comment.author = g.Front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这篇帖子')
    else:
        return restful.params_error(message=form.get_error())


#点赞
@bp.route('/praise/',methods=['POST'])
@login_required
def user_praise():
    form = PraiseForm(request.form)
    if form.validate():
        post_id = form.post_id.data
        fuser_id = form.fuser_id.data
        post = PostModel.query.filter_by(id=post_id).first()
        fuser = FrontUser.query.filter_by(id=fuser_id).first()

        if post and fuser:
            praise_pid = PraiseModel.query.filter_by(post_id=post_id).first()
            praise_uid = PraiseModel.query.filter_by(fuser_id=fuser_id).first()
            if praise_pid and praise_uid:
                return restful.params_error(message="用户重复点赞!")
            else:
                config.PRAISW_COUNT = config.PRAISW_COUNT + 1
                now_praise = PraiseModel(fuser_id=fuser_id,post_id=post_id)
                post.praise_count = config.PRAISW_COUNT
                db.session.add(now_praise)
                db.session.commit()
                return restful.success()
        else:
            return restful.params_error(message="帖子或用户不存在")
    else:
        return restful.params_error(message=form.get_error())

#取消点赞
@bp.route('/c_praise/',methods=['POST'])
@login_required
def cancelpraise():
    form = PraiseForm(request.form)
    if form.validate():
        post_id = form.post_id.data
        fuser_id = form.fuser_id.data
        praise = PraiseModel.query.filter_by(post_id=post_id).first()
        post = PostModel.query.filter_by(id=post_id).first()
        if praise:
            count = post.praise_count - 1
            post.praise_count = count
            db.session.delete(praise)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这篇帖子！")
    else:
        return restful.params_error(message=form.get_error())




class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer #获取上一个页面的url
        if return_to and return_to != request.url and safetool.is_safe_url(return_to):
            return render_template('front/front_signup.html',return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password1 = form.password1.data
            user = FrontUser(telephone=telephone,username=username,password=password1)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            # message = form.get_error().popitem()[1][0]
            message = form.get_error()
            print(form.get_error())
            return restful.params_error(message=message)


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safetool.is_safe_url(return_to)and url_for('front.signup'):
            return render_template('front/front_signin.html',return_to=return_to)
        else:
            return render_template('front/front_signin.html')
    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机或密码错误！')
        else:
            return restful.params_error(form.get_error())

bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/',view_func=SigninView.as_view('signin'))
