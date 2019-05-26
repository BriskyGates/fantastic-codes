class DB:
    def __init__(self, host, user, password, db):
        self.host=host
        self.user=user
        self.password = password
        self.db = db    
        self.conn()
        
    def conn(self):
        self.connect = pymysql.Connect(host=self.host,
                                       port=3306,
                                       user=self.user,
                                       password=self.password,
                                       db=self.db,
                                       charset='utf8')
        
    def __enter__(self):
        return self.connect.cursor()
    
    def __exit__(self, exc, value, traceback):
        print('------__exit__-------', exc, value)
        # exc -> pymysql.err.ProgrammingError
        # 在此方法中，是否可以处理掉exc异常对象？？？
        # traceback 的对象属性或方法有哪些 ？
        if exc:
            self.connect.rollback()
        else:
            self.connect.commit()
            self.connect.close()
			
"""
1.实例化数据库连接对象
2.利用python上下文要经历的__enter__(),
	__exit__()来获得数据库连接的cursor对象,执行原生sql查询
	和关闭cursor对象,和connect对象
"""
with DB('127.0.0.1', 'root', 'root', 'stu') as cursor:
	cursor.execute('select * from A2')
	for row in cursor.fetchall():
		print(row)
