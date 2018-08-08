#登录限制装饰器
from functools import wraps
from flask import session,redirect,url_for,g
import config
def login_required(func):
    @wraps(func)
    def limit(*args,**kwargs):
        if config.CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return limit

#没有权限通过url的方式也不能访问，使用以下装饰器限制
def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter