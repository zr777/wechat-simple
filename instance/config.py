# -*- coding: utf-8 -*-
# attention: No chinese
# otherwise will raise an ecxeption
# remeber to remove the chinese annotion for production
from celery.schedules import crontab

DEBUG = False

# wechat public platform configuration
APP_ID = ""
APP_SECRET = ""
TOKEN = ""
AES_KEY = ""

# http://docs.sqlalchemy.org/en/rel_1_0/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql
# SQLALCHEMY_DATABASE_URI = \
# "mysql+pymysql://root:1q2w3eguo@localhost/wx?charset=utf8mb4"
# http://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
# SQLALCHEMY_TRACK_MODIFICATIONS = True

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULE = {
    'every-1-min': {
        'task': 'get_news',
        'schedule': 30.0
    },
}
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
# CELERYBEAT_SCHEDULE = {
#     'every-1-hour-at-6-to-22': {
#         'task': 'get_news',
#         'schedule': crontab(minute=0, hour='6-22')
#     },
# }
