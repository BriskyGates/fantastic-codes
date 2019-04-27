# -*- coding:utf-8 -*-
import redis

class RedisNews(object):
    def __init__(self):  # 创建连接redis数据库的实例方法
        # 返回的是二进制类似 b'\xe..'(返回字节类型),
        # 需要添加decode_responses=True(返回str类型,可以识别中文字符)
        try:
            self.r = redis.StrictRedis(host='47.101.219.50', port=6379, decode_responses=True)

        except Exception as e:
            print('Redis connect failed')

    def _news_id(self, int_id):
        # 返回  news:新闻id  的数据
        return 'news:%d' % int(int_id)

    def _news_type(self, news_type):
        # 返回  news_type:新闻类型  的数据
        return 'news_type:%s' % news_type

    def _news_list_name(self):
        # 返回 新闻列表 名称
        return 'news'

    # 新增新闻数据
    def add_news(self, news_obj: dict):
        int_id = self.r.incr('news_id')  # int_id(作为news_id)从0开始自增
        news_id = self._news_id(int_id)  # _news_id()把news_id为int
        # 用散列类型存储  每条新闻数据
        self.r.hmset(news_id, news_obj)
        # 用列表存储  每条新闻的id
        self.r.rpush(self._news_list_name(), int(int_id))

        news_type = self._news_type(news_obj['news_type'])
        # 用集合存储  每种新闻类型下的新闻id(集合去重)
        self.r.sadd(news_type, int_id)
        print('成功添加新闻数据')
        return self.r  # 返回Redis数据库连接实例,你可以进行查找相关数据

    # 用事务添加新闻数据
    # 可以通过管道pipeline获取,而不是通过连接获取
    def add_news_with_trans(self, new_obj):
        try:
            pipe = self.r.pipeline()
            int_id = pipe.incr('news_id')
            news_id = f'news:{int_id}'  # 也可以使用_news_id(int_id)来解决
            rest = pipe.hmset(news_id, new_obj)
            pipe.rpush(self._news_list_name(), int_id)
            news_type = self._news_type(new_obj['news_type'])
            pipe.sadd(news_type, int_id)
            # 事务执行返回结果给result
            result = pipe.execute()  # 以列表返回[conn, stack, raise_on_error] 数据
            """
            [True, 1, 1]
            [True, 2, 1]
            [True, 3, 1]
            """
            print('使用事务成功添加新闻数据')
            return result
        except Exception as e:
            print(e)
            print('出现异常,无法使用pipeline添加新闻数据')

    # 模拟新闻首页,获取全部数据
    def get_all_news(self):
        news_id_list = self.r.lrange(self._news_list_name(), 0, -1)
        news_list = []
        for int_id in news_id_list:
            news_id = self._news_id(int_id)
            data = self.r.hgetall(news_id)  # 获取某key的所有信息(包括field和value)
            data['id'] = int_id  # 为每条新闻添加id
            news_list.append(data)
        return news_list

    # 分类页
    def get_news_by_cat(self, news_type):
        news_id_list = self.r.smembers(self._news_type(news_type))
        news_list = [self.r.hgetall(self._news_id(int_id)) for int_id in news_id_list]
        return news_list

    # 详情页--根据新闻拆来获取某一条新闻详情
    def get_news_by_id(self, int_id):
        news_id = self._news_id(int_id)
        data = self.r.hgetall(news_id)
        data['id'] = int_id
        return data

    # 后台首页和分页
    def paginate(self, page=1, per_page=10):  # 默认第一页,每页展示10条新闻

        if not page:  # 避免用户输入[],{},"" etc.
            page = 1
        news_list = []
        start = (page - 1) * per_page  # start从0开始
        end = page * per_page - 1
        news_id_list = self.r.lrange(self._news_list_name(), start, end)  # lrange()包左包右,start 为开始下标,即id为1
        news_list = [self.r.hgetall(self._news_id(int_id)) for int_id in news_id_list]

        return news_list, page, per_page

    # 新闻的删除
    def delete_by_id(self, int_id):
        if not self.check_id(int_id):
            return 'id不存在 or 没有可删除的新闻'
        try:
            pipe = self.r.pipeline()
            pipe.decr('news_id')
            pipe.lrem(self._news_list_name(), 1, int_id)  # 第二个参数为删除次数
            news_id = self._news_id(int_id)
            news_type = self.r.hget(news_id, 'news_type')  # 要删除集合中的该元素,得知道其news_type
            pipe.srem(news_type, int_id)
            pipe.delete(news_id)
            print(f'{int_id}相关记录删除成功')
            return pipe.execute()  # 四条执行信息
        except Exception as e:
            print(e)
            print('出现异常,无法使用pipeline删除某一新闻')

    # 新闻内容的修改--不能修改id,你可以修改一条数据(field,value),也可以修改多条数据(多个field,value)
    def correct_news_by_id(self, int_id, **kwargs):

        if not self.check_id(int_id):
            return 'id不存在 or 没有可删除的新闻'
        keys = self.print_news_keys(int_id)

        if set(kwargs.keys()) - keys:
            return 'opps,你添加了未知的field哦.请检查你的field'

        news_id = self._news_id(int_id)
        try:
            self.r.hmset(news_id, kwargs)
            print('修改数据成功')
        except Exception as e:
            print(e)
            print('修改新闻数据失败')

    def print_news_keys(self, int_id):
        print('你可以修改新闻的以下内容哦:)')
        news_keys = self.r.hkeys(self._news_id(int_id))
        for i in news_keys:
            print(i)
        return set(news_keys)

    def check_id(self, int_id):
        if self.r.llen(self._news_list_name()) == 0:  # 此处使用pipe不能返回具体的值,而只能是StrictPipeline对象
            return False
        elif str(int_id) not in self.r.lrange(self._news_list_name(), 0, -1):  # 列表中的每个元素是字符串
            return False
        else:
            return True  # 默认返回None
