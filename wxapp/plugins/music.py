# -*- coding: utf-8 -*-
import requests


def get_douban_fm():
    """抓取豆瓣FM, 返回带链接的文本消息"""
    url = 'https://douban.fm/j/v2/playlist?' + \
        'app_name=radio_website&version=100&channel=0&type=n'
    try:
        r = requests.get(url, timeout=3)
        result = r.json()["song"][0]
        desc = result["artist"] + u'-建议WiFi下播放'
        music_url = result["url"]
        title = result["title"]
        content = u'<a href="{url}">{title}</a>\n - {desc}'.format(
            url=music_url, title=title, desc=desc
        )
    except Exception as e:
        print(u"douban FM failure: %s" % e)
        content = u"网络繁忙，请稍候重试"
    return content
