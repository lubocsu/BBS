import os
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'BBS'
USERNAME = 'root'
PASSWORD = 'root'

BR_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOSTNAME,port=PORT,db=DATABASE)
SQLALCHEMY_DATABASE_URI = BR_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(24)

CMS_USER_ID = 'aaa'
FRONT_USER_ID = 'bbb'

#配置发送邮箱服务器地址信息
#MAIL_USE_TLS:端口号 587
#MAIL_USE_SSL：端口号 465
#发送者邮箱地址
MAIL_SERVER ='smtp.qq.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL : default False
MAIL_USERNAME = '243246973@qq.com'
MAIL_PASSWORD = 'llwvyvfkgcgncajh'
MAIL_DEFAULT_SENDER = '243246973@qq.com'

# 阿里短信
# -*- coding: utf-8 -*-
import uuid
business_id = uuid.uuid1()
# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = "LTAINCUC7oTRd5GE"
ACCESS_KEY_SECRET = "OlQBJxWmEy3Jfv3UJXYdUYoNobfLEr"
BUSINESS_ID =  business_id
SIGN_NAME = '周俊宇'
TEMPLATE_CODE = 'SMS_139575022'

#ueditor上传图片配置信息
UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')
# UEDITOR_UPLOAD_TO_QINIU = True
# UEDITOR_QINIU_ACCESS_KEY = "VUqezRGdo0N_78MAn3DS5bO7n2uNI7E86OiGz8Df"
# UEDITOR_QINIU_SECRET_KEY = "fiuQZzcWWplmEb_0kW3IcyH5jjN6nXb6Opz19zB5"
# UEDITOR_QINIU_BUCKET_NAME = "banners"
# UEDITOR_QINIU_DOMAIN = "http://pc5nfgg9w.bkt.clouddn.com/"

#flask-pggination 帖子分页配置
PER_PAGE = 10
PRAISW_COUNT = 0

#flask celery相关配置
CELERY_RESULT_BACKEND = "redis://:zjy@192.144.41.105:6379/0"
CELERY_BROKER_URL = "redis://:zjy@192.144.41.105:6379/0"