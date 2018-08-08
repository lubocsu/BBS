from .views import bp
from flask import session,g,render_template
from .models import FrontUser
import config
#用户信息绑定G对象
#钩子函数 在预编译时执行以下函数
@bp.before_request
def before_request():
    if config.FRONT_USER_ID in session:
        user_id = session.get(config.FRONT_USER_ID)
        user = FrontUser.query.get(user_id)
        if user:
            g.Front_user = user


#404页面处理函数
@bp.errorhandler(404)
def page_not_found(error):
    return render_template('front/front_404.html'),404