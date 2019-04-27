# -*- coding:utf-8 -*-
# 不在开头添加会出现SyntaxError: Non-UTF-8 code starting with '\xe5' in file错误
from redis_news import RedisNews

from delicate_test.news_data import test_data, list_news

if __name__ == '__main__':
    redis_news = RedisNews()
    # for item in list_news:
    # 每条item都是add_news()的Redis数据库连接实例进行相关操作的
    # redis_news.add_news(item)
    #     result_trans=redis_news.add_news_with_trans(item)
    #     print(result_trans)
    # redis_news.delete_by_id(6)
    correct_news = redis_news.correct_news_by_id(1, **test_data)

    # news_id=redis_news.get_news_by_id(1)
    # news_cat=redis_news.get_news_by_cat('推荐')
    # all_news=redis_news.get_all_news()
