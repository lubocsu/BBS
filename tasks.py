#celery实现异步发送邮箱验证码和短信验证码
#注意不能从BBS.py中直接导入app,会造成循环引入，必须重新生成一个app

from celery import Celery
from flask_mail import Message
from exts import mail
from flask import Flask
import config

app=Flask(__name__)
app.config.from_object(config)
mail.init_app(app)
#该函数创建一个新的Celery对象，使用代理配置中的代理进行配置，从Flask配置更新Celery配置的其余部分，然后创建任务的子类，将任务执行包装在应用程序上下文中
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)
#创建一个任务
@celery.task
def send_mail(subject,recipients,body):
    message =Message(subject=subject,recipients=recipients,body=body)
    mail.send(message)