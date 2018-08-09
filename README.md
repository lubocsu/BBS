# 区块链论坛项目

## 简介
本项目由前后台组成，前台实现了基本的论坛操作（登录，注册，轮播图，各个板块下的帖子显示，用户信息查看和修改，发帖，点赞，评论等功能），后台是CMS管理系统
主要实现了管理人员的权限分配和限制，个人信息查看和修改，前台板块管理，前台帖子管理，前台轮播图的管理等功能。是我学习flask时候练手项目

## 主要用到的技术
python3+flask框架，前端html+css+bootstrap框架+js+jq+ajax,前端弹窗用的是sweetalert2，注册界面短信验证码调用的是阿里大鱼短信接口，图形验证码是用
python中PIL图形处理工具画的，验证码缓存是用的memcache,用celery+redis来异步完成发送短信验证码和邮箱验证码操作，用户上传的图片调用的七牛接口等等

## 使用方法
* 克隆到本地
```
https://github.com/zjy959/BBS.git
```
* 安装虚拟环境
```
[virtualenv安装]（http://note.youdao.com/noteshareid=652c010229541f9ac8f269b97b32d907&sub=F8DD453C58AD499DAF9C5FD92FE9FAEE）
```
* 用pycharm打开你克隆的项目
```
在pycharm底部打开Terminal，然后进入到你的虚拟环境如workon my_env
```
```
我们在执行这条命令：pip install -r requirements.txt
```
* 假定大家都安装好了MySQL，我们去创建一个databases,在mysql命令行中输入：
```
create database you_database_name charset urf-8;
```
* 修改下我们的配置文件，config中的数据库配置
```
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'you_database_name'
USERNAME = 'root（你的数据库用户名）'
PASSWORD = 'root（你的数据库密码）'
```
* 使用Flask中强大的sqlalchemy -> Flask-Migrate；来实现数据库的迁移
```
python manage.py db init     # 创建迁移的仓库
Python manage.py db migrate  # 创建迁移的脚本
python manage.py db upgrade  # 更新数据库
```
* 然后我们添加下后台CMS管理系统的人员
```
python manage.py create_cms_user -u xxx(自己设置用户名) -p xxx（自己设置密码） -e xxx@qq.com（自己设置邮箱地址）
```
* 给管理人员增加权限角色
```
我只设定了四种角色：游客，运营，管理员，和开发者，每个角色有不同的权限，具体看apps/cms/models中的CMSpermission这个类
```
```
命令添加操作：python manage.py add_user_to_role -e test@qq.com（这是我当前的测试邮箱，具体根据你自己的） -n 运营（四个角色中其中一个）
```
* 配置邮箱，memched,celery+redis,七牛，阿里云的相关信息，百度的富文本编辑器
```
具体在config.py文件有详情的注释
```
* 最后运行BBS.py这个文件，打开http://127.0.0.1:5000, 成功啦

## 网站的截图
