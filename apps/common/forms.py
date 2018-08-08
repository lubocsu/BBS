from apps.forms import BoseForm
from wtforms import StringField
from wtforms.validators import regexp,InputRequired,ValidationError
from ..front.models import FrontUser
# from tool import restful
import hashlib
class SMSCaptchaForm(BoseForm):
    salt ='12#dfdsaddddp'
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])#时间戳
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SMSCaptchaForm,self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        user = FrontUser.query.filter_by(telephone=telephone).first()
        # print('+++++++++++++++++++++')
        # print(type(user.telephone))
        # print('++++++++++++++++++')
        #md5(timestamp+telephone+salt)
        #md5函数必须要传一个bytes类型的字符串进去
        sign2 = hashlib.md5((timestamp+telephone+self.salt).encode('utf-8')).hexdigest()
        if user != None:
            return 1
        elif sign == sign2:
            return 2
        else:
            return False