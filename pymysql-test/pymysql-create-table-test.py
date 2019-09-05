# connect the mysql with pymysql

import pymysql

# connect the db
conn = pymysql.connect(host="192.168.10.200", user="root", password="root", database="selenium",charset="utf8")

# 得到一个可以执行sql语句的光标对象
cursor = conn.cursor() # 执行完毕返回的结果集默认以元组显示
# 得到一个可以执行sql语句并且讲结果作为字典返回的游标
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# 写sql
sql = """
CREATE TABLE article (
id INT auto_increment PRIMARY KEY,
author char(50) NOT NULL,
content text NOT NULL
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""

sql1 = """
CREATE TABLE girl (
id INT auto_increment PRIMARY KEY,
image char(200) NOT NULL,
url char(200) NOT NULL,
download_flag INT NOT NULL
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""
# 执行sql
cursor.execute(sql1)


# 关闭光标对象
cursor.close();

# 关闭数据库链接
conn.close()

