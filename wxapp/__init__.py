# -*- coding: utf-8 -*-
from flask import Flask
from redis import Redis
from .utils import make_celery


app = Flask(__name__, instance_relative_config=True)
# 加载配置
# https://spacewander.github.io/explore-flask-zh/5-configuration.html
# with virtualenv see :
# http://stackoverflow.com/questions/31164127/unable-to-load-configuration-file-from-instance-folder-when-deploying-app
app.config.from_object('config')  # 加载微信公众号一般信息，如菜单栏配置等
app.config.from_pyfile('config.py')  # 从instance文件夹中加载秘密配置信息，如app-token等

# app.register_blueprint(wxbase, url_prefix='/wx')

# 队列
# http://docs.jinkan.org/docs/celery/getting-started/first-steps-with-celery.html#first-steps
celery = make_celery(app)

# 初始第三方库
# https://github.com/andymccurdy/redis-py
redis = Redis()

# 加载url路由，位于views文件夹中
from .views.wxbase import *
# 使用blueprints遭遇app.config获取的问题，暂未解决
from .tasks import *
