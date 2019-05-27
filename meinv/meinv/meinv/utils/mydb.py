import pymysql

config = {
    'host': '47.101.219.50',
    'port': 3306,
    'user': 'root',
    'password': 'lifei',
    'charset': 'utf8',
    'db': 'test'
}

create_table_sql = """
create TABLE t_mv(id int PRIMARY KEY auto_increment, name VARCHAR(255), image_path VARCHAR(255));
"""

exists_table_sql = """
select table_name from information_schema.tables where TABLE_NAME = %s
"""

insert_sql = """
insert t_mv(name, image_path) values (%s, %s)
"""

class DB():
    def __init__(self):

        self.conn = pymysql.connect(**config)

        with self.conn as cursor:

            cursor.execute(exists_table_sql, 't_mv')
            if len(cursor.fetchall()) == 0:
                cursor.execute(create_table_sql) # 创建数据库存放数据

        print('---init db ok---')

    def add(self, item):
        # print('99999999999999')
        print('正在添加数据')
        with self.conn as cursor:
            # 往数据库中插入数据
            # item['images']包括两个元素,报错:InternalError: (1241, 'Operand should contain 1 column(s)')
            if len(item['images']) > 1:
                item['images'] = '##'.join(item['images'])  # 以## 作为分隔符分割多张个图片途径
            cursor.execute(insert_sql, args=(item['star_name'], item['images']))

        self.conn.commit()