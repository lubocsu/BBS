# 表单验证
from wtforms import StringField,IntegerField,ValidationError
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BoseForm
from tool import zzcache
from flask import g

class LoginForm(BoseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='请输入正确的密码格式')])
    remember = IntegerField()
class ResetpwdForm(BoseForm):
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式的新密码')])
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd',message="两次密码不一致")])

class ResetemailForm(BoseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式')])
    captcha = StringField(validators=[Length(6,6,message='验证码格式错误')])
    #当执行captcha表单验证时同时也会执行validate_captcha函数来验证
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zzcache.get(email) #从memcached中获取email所对应的验证码
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')
    def validate_email(self,field):
        email = field.data
        user = g.cms_user #通过g对象来获取数据库中用户原邮箱名
        if user.email == email:
            raise ValidationError('新邮箱不能和旧邮箱相同')

class AbannerForm(BoseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_b = StringField(validators=[InputRequired(message='请输入轮播图图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级！')])

class UbannerForm(AbannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id!')])


class AddBoardForm(BoseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名')])


class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])

class DeleteBoardForm(UpdateBoardForm):
    pass