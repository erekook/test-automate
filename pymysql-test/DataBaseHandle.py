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
       except Exception as e:
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
       except Exception as e:
            print(e)
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
       except Exception as e:
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
       except Exception as e:
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
            return data
            # 遍历结果
       except Exception as e:
            self.db.rollback()
            print('Error: unable to fetch data')
       finally:
            self.cursor.close()


    def closeDB(self):
        self.db.close()

if __name__ == '__main__':

    dbHandle = DataBaseHandle('192.168.10.200', 'root', 'root', 'selenium', 3306)
    sqlArgs = [['author001','content01',0,'title01'], ['author002','content02',0,'title02']]
    dbHandle.insertManyDB('insert into girl(image,url,download_flag,title) values(%s,%s,%s,%s)', sqlArgs)
    #results = dbHandle.selectDB('select * from article')
    #print(results)
