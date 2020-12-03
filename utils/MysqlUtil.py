import pymysql
# 1、创建封装类
from config import Conf
from utils.LogUtil import my_log


class Mysql:
# 2、初始化数据，连接数据库，光标对象
    def __init__(self, host, user, password, database, charset="utf8", port=3306):
        self.log = my_log()
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            port=port
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
# 3、创建查询、执行方法
    def fetchone(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def fetchmany(self,sql,size):
        self.cursor.execute(sql)
        return self.cursor.fetchmany(sql,size)

    def exec(self, sql):
        try:
            if self.conn and self.cursor is not None:
                self.cursor.execute(sql)
                # self.cursor.commit()
        except Exception as ex:
            self.conn.rollback()
            self.log.error("Mysql 执行失败")
            self.log.error(ex)
            return False
        return True

# 4、关闭对象
    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

if __name__ == "__main__":
    db_info = Conf.ConfigYaml().get_db_config_info("db_1")
    # 2、初始化数据库信息，通过配置
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = int(db_info["db_port"])

    # 3、初始化mysql对象
    mysql = Mysql(host, user, password, name, charset, port)
    re = mysql.exec("update goods set name ='Chinese' where id =1")
    r = mysql.fetchone("select * from goods")
    print(re)
    print(r)

    # 1、创建db_conf.yml, db1,db2
    # 2、编写数据库基本信息
    # 3、重构Conf.py
    # 4、执行
# 1、导入pymysql包

# 2、连接database
# conn = pymysql.connect(
#     host="123.207.107.xxx",
#     user="root",
#     password="root",
#     database="apitest",
#     charset="utf8",
#     port=3306
#
# )
# # 3、获取执行sql的光标
# cursor = conn.cursor()
# # 4、执行sql
# sql = "select * from goods"
# cursor.execute(sql)
# result = cursor.fetchall()
# print(result)
# # 5、关闭对象
# cursor.close()
# conn.close()