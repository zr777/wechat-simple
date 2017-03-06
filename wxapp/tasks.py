# -*- coding: utf-8 -*-
from wxapp import celery, redis
import pickle
import feedparser


@celery.task(name="get_news")
def get_news():
    """获取最新的学院新闻"""
    redis_key = 'wechat:news'
    BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
    feed = feedparser.parse(BBC_FEED)
    news = [
        {
            'title': i.title,
            'description': i.summary,
            'url': i.link,
            'picurl': i.media_thumbnail[0]['url'],
        } for i in feed['entries'][:10]
    ]
    content = pickle.dumps(news)
    redis.set(redis_key, content)
    # g.client_.message.send_articles(g.openid_, news) 主动消息 需要权限
