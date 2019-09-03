### 封装pymysql的增删改查

import pymysql

class DataBaseHandle(object):
    '''定义一个Mysql 操作类'''
       
    # 在创建类的实例的时候，实例会自动调用这个方法，一般用来对实例的属性进行初始化
    def __init__(self, host, username, password, database, port):
        '''初始化数据库信息并创建数据库连接'''
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, self.port, charset="utf8")
    
    '''插入'''
    def insertDB(self, sql):
       self.cursor = self.db.cursor()
       try:
            # exec sql
            self.cursor.execute(sql)
            self.db.commit()
       except:
            self.db.rollback()
       finally:
            self.cursor.close()

    '''插入多行'''
    def insertManyDB(self, sql, args):
       self.cursor = self.db.cursor()
       try:
            # exec sql
            self.cursor.executemany(sql, args)
            self.db.commit()
       except:
            self.db.rollback()
       finally:
            self.cursor.close()

    '''删除'''
    def deleteDB(self, sql):
       self.cursor = self.db.cursor()
       try:
            # exec sql
            self.cursor.execute(sql)
            self.db.commit()
       except:
            self.db.rollback()
       finally:
            self.cursor.close()

    '''更新'''
    def updateDB(self, sql):
       self.cursor = self.db.cursor()
       try:
            # exec sql
            self.cursor.execute(sql)
            self.db.commit()
       except:
            self.db.rollback()
       finally:
            self.cursor.close()

    '''查询'''
    def selectDB(self, sql):
       self.cursor = self.db.cursor()
       try:
            # exec sql
            self.cursor.execute(sql)
            data = self.cursor.fetchall() # 返回所有记录列表
            print('results:', data)

            # 遍历结果
       except:
            print('Error: unable to fetch data')
       finally:
            self.cursor.close()


    def closeDB(self):
        self.db.close()

if __name__ == '__main__':

    dbHandle = DataBaseHandle('192.168.10.202', 'root', 'root', 'selenium', 3306)
    sqlArgs = [['author001','content01'], ['author002','content02']]
    dbHandle.insertManyDB('insert into article(author,content) values("%s","%s")', sqlArgs)
