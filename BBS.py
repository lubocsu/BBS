from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from apps.ueditor import bp as ueditor_bp
from exts import db,mail
from flask_wtf import CSRFProtect
# from tool.captcha import Captcha
import config
#定义一个工厂函数
def create_app():
    app = Flask(__name__)
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(ueditor_bp)
    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    return app
# @app.route('/')
# def hello_world():
#     return 'Hello World!'

# Captcha.gene_captcha()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
