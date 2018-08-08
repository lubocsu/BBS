from .views import bp
from flask import session,g
from .models import CMSUser,CMSpermission
import config
#用户信息绑定G对象
#钩子函数 在预编译时执行以下函数
@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user
@bp.context_processor
def cms_context_processor():
    return {"CMSpermission":CMSpermission}