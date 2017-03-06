from wxapp import app
from flask import request, abort, g
from wechatpy import parse_message, create_reply
# from wechatpy import WeChatClient
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
import re

# blueprint for refractor
# https://spacewander.github.io/explore-flask-zh/7-blueprints.html

TOKEN = app.config['TOKEN']
AES_KEY = app.config['AES_KEY']
APP_ID = app.config['APP_ID']
APP_SECRET = app.config['APP_SECRET']


# https://github.com/jxtech/wechatpy/blob/master/examples/echo/app.py
@app.route("/wx", methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', 'raw')
    msg_signature = request.args.get('msg_signature', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        return echo_str

    # POST request
    if encrypt_type == 'raw':
        # plaintext mode
        msg = parse_message(request.data)
        return wechat_response(msg)
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APP_ID)
        try:
            msg = crypto.decrypt_message(
                request.data,
                msg_signature,
                timestamp,
                nonce
            )
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            return crypto.encrypt_message(wechat_response(msg),
                                          nonce,
                                          timestamp)


def wechat_response(msg):
    """微信消息处理回复"""

    g.msg_ = msg
    # g.openid_ = msg.source
    # 用户信息写入数据库
    # set_user_info(openid)
    try:
        # 获取相应类型的回复函数
        if msg.type == "event":
            resp_func = msg_type_resp[msg.event]
        else:
            resp_func = msg_type_resp[msg.type]
        response = resp_func()  # 回复函数从g中获取消息对象
    except KeyError:
        # 默认回复微信消息
        response = 'success'

    # 保存最后一次交互的时间
    # set_user_last_interact_time(openid, message.time)
    return response


# def init_client():
#     """生成发送主动消息的客户端, 需要认证后才有权限"""
#     if not getattr(g, 'client_', None):
#         g.client_ = WeChatClient(APP_ID, APP_SECRET)


###########################################################################
# 储存微信消息类型所对应函数（方法）的字典
msg_type_resp = {}


def set_msg_type(msg_type):
    """
    储存微信消息类型所对应函数（方法）的装饰器
    """
    def decorator(func):
        msg_type_resp[msg_type] = func
        return func
    return decorator


@set_msg_type('text')
def text_resp():
    """文本类型回复"""
    # 默认回复微信消息
    response = ''
    msg = g.msg_
    # 替换全角空格为半角空格
    msg.content = msg.content.replace(u'　', ' ')
    # 清除行首空格
    msg.content = msg.content.lstrip()
    # 指令列表
    commands = {
        u'新闻|新聞': get_news,
        u'音乐|音樂': play_music,
        u'游戏': html5_games,
        u'^\?|^？': all_command,
    }
    # 匹配指令
    for key_word in commands:
        if re.search(key_word, msg.content):
            response = commands[key_word]()
            break
    if not response:
        response = create_reply(
            '咩？\n\n' + app.config['COMMAND_TEXT'],
            g.msg_
        ).render()
    return response


# @set_msg_type('click')
# def click_resp():
#     """菜单点击类型回复"""
#     msg = g.msg_
#     commands = {
#         'news': get_news,
#         'game': html5_games,
#         'music': play_music,
#     }
#     # 匹配指令后，重置状态
#     # set_user_state(openid, 'default')
#     response = commands[msg.key]()
#     return response


@set_msg_type('subscribe')
def subscribe_resp():
    """订阅类型回复"""
    content = app.config['WELCOME_TEXT'] + app.config['COMMAND_TEXT']
    return create_reply(content, g.msg_).render()


#######################################################################


from wxapp.plugins import music
import pickle
from wxapp import redis


def play_music():
    """随机音乐"""
    return create_reply(
        music.get_douban_fm(),
        g.msg_
    ).render()


def get_news():
    """读取学院新闻"""
    redis_key = 'wechat:news'
    news_cache = redis.get(redis_key)
    if news_cache:
        news = pickle.loads(news_cache)
        content = ''
        for index, i in enumerate(news):
            content += '{index}. - <a href="{url}">{title}</a>\n'.format(
                title=i['title'],
                url=i['url'],
                index=index,
            )
        return create_reply(
            content,
            g.msg_
        ).render()
    else:
        return create_reply(
            u'您要的新闻正在准备中',
            g.msg_
        ).render()


def html5_games():
    """HTML5游戏"""
    content = app.config['HTML5_GAMES_TEXT'] + app.config['HELP_TEXT']
    return create_reply(content, g.msg_).render()


def all_command():
    """回复全部指令"""
    content = app.config['COMMAND_TEXT']
    return create_reply(content, g.msg_).render()
