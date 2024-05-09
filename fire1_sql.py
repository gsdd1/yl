import pymysql
from PyQt5.QtSql import QSqlQuery, QSqlDatabase


class OperationMysql:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName('127.0.0.1')
        self.db.setPort(3306)
        self.db.setUserName('root')
        self.db.setPassword('123456')
        self.db.setDatabaseName('yolov')

    def open_connection(self):
        if self.db.open():
            print("数据库连接成功")
        else:
            print("数据库连接失败")

    def search(self, sql):
        query = QSqlQuery(self.db)
        if query.exec_(sql):
            result = query.fetchAll()
            return result
        else:
            print("查询失败:", query.lastError().text())
            return None

    def update_one(self, sql):
        query = QSqlQuery(self.db)
        if query.exec_(sql):
            self.db.commit()
            return True
        else:
            self.db.rollback()
            return False

    def search(self, sql):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()
                return result

    # 更新SQL
    def update_one(self, sql):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(sql)  # 执行sql
                    self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
                except:
                    # 发生错误时回滚
                    self.conn.rollback()

    # 插入SQL
    def insert_one(self, sql):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(sql)  # 执行sql
                    self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
                except:
                    # 发生错误时回滚
                    self.conn.rollback()

    # 删除sql
    def delete_one(self, sql):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(sql)  # 执行sql
                    self.conn.commit()  # 增删改操作完数据库后，需要执行提交操作
                except Exception as e:
                    # 发生错误时回滚
                    print("Error:", e)
                    self.conn.rollback()

