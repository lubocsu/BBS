from ..forms import BoseForm
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp,EqualTo,ValidationError,InputRequired
from tool import zzcache

class SignupForm(BoseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}',message='请输入正确格式的手机号码')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}',message='请输入正确格式的短信验证码')])
    username = StringField(validators=[Regexp(r'.{2,20}',message='请输入正确格式的用户名')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}',message='请输入正确格式的密码')])
    password2 = StringField(validators=[EqualTo('password1',message='两次密码输入不一致')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式的验证码')])

    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data
        if sms_captcha != '1111': #测试代码
            #从memecache中取验证码
            sms_captcha_mem = zzcache.get(telephone)
            if not sms_captcha_mem or sms_captcha.lower() != sms_captcha_mem.lower():
                super(SignupForm, self).get_error()
                raise ValidationError(message='短信验证码错误！')
    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        if graph_captcha != '1111':  # 测试代码
            graph_captcha_mem = zzcache.get(graph_captcha.lower())
            if not graph_captcha_mem:
                super(SignupForm, self).get_error()
                raise ValidationError(message='图形验证码错误！')


class SigninForm(BoseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message='请输入正确格式的手机号码')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='请输入正确格式的密码')])
    remember = StringField()


class AddPostForm(BoseForm):
    title = StringField(validators=[InputRequired(message='请传入标题！')])
    content = StringField(validators=[InputRequired(message='请传入内容！')])
    board_id = IntegerField(validators=[InputRequired(message='请传入板块id!')])

class AddCommentForm(BoseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容！')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])

class PraiseForm(BoseForm):
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])
    fuser_id = StringField(validators=[InputRequired(message='请传入用户id！')])

class CancelPraiseForm(BoseForm):
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])
    fuser_id = StringField(validators=[InputRequired(message='请传入用户id！')])