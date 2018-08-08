from flask import Blueprint,request,make_response,jsonify
from tool.dysms_python import demo_sms_send
from tool import restful,zzcache
from tool.captcha import Captcha
from .forms import SMSCaptchaForm
from io import BytesIO #专门写二进制流数据
import json,qiniu
bp = Blueprint("common",__name__,url_prefix='/c')

@bp.route('/')
def index():
    return 'common index'

#   get请求不安全，别人轻易可以调用你的接口
# @bp.route('/sms_captcha/')
# def sms_captcha():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请传入手机号码')
#     captcha = Captcha.gene_text(4)
#     params = json.dumps({'code': captcha}) #将 Python 对象编码成 JSON 字符串
#     print(params)
#     result = demo_sms_send.send_sms(telephone,params)
#     print(type(result))
#     resu=str(result,encoding='utf-8') #bytes转字符串
#     print(resu)
#     params2 = json.loads(resu) #JSON到字典转化
#     # print(params['Code'])
#     if params2['Code'] == 'OK':
#         return restful.success()
#     else:
#         return restful.params_error(message='短信验证码发送失败')
@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate() == 1:
        return restful.params_error(message='号码已存在！')
    if form.validate() == 2:
        telephone = form.telephone.data
        captcha = Captcha.gene_text(4)
        params = json.dumps({'code': captcha})  # 将 Python 对象编码成 JSON 字符串
        print(params)
        result = demo_sms_send.send_sms(telephone,params) #发送验证码
        print(type(result))
        resu=str(result,encoding='utf-8') #bytes转字符串
        print(resu)
        params2 = json.loads(resu) #JSON到字典转化
        if params2['Code'] == 'OK':
            zzcache.set(telephone, captcha) #将验证码存入memcache
            return restful.success()
        else:
            # zzcache.set(telephone, captcha)  # 将验证码存入memcache
            return restful.params_error(message='短信验证码发送失败')
    else:
        return restful.params_error(message='参数错误！！！')

@bp.route('/captcha/')
def graph_captcha():
    #获取验证码
    image,text = Captcha.gene_captcha()
    zzcache.set(text.lower(),text.lower(),120)
    print(text)
    #BytesIO 创建字节流对象
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'#指定response对象内容类型
    return resp

#上传七牛图片接口
@bp.route('/uptoken/')
def uptoken():
    access_key = 'VUqezRGdo0N_78MAn3DS5bO7n2uNI7E86OiGz8Df'
    secret_key = 'fiuQZzcWWplmEb_0kW3IcyH5jjN6nXb6Opz19zB5'
    q = qiniu.Auth(access_key,secret_key)
    bucket = 'banners'
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})