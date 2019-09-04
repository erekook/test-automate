from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
sys.path.append('../pymysql-test/')
from DataBaseHandle import *

class QsbkSpider(object):
    

    def __init__(self):
        '''init data'''
        # 解决在root下无法打开chrome的问题
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        # Create a new instance of the Chrome driver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.sqlArgs = []
        self.page = 0

    # 爬取内容 
    def parse(self):
        self.page += 1
        # 文章列表
        articleWebElementList = self.driver.find_elements_by_class_name("article")
        # 第一个文章的作者
        #author = articleBoxs[0].find_element_by_tag_name("h2")
        # 第一个文章的内容
        #content = articleBoxs[0].find_element_by_tag_name("span")
        #print(content.get_attribute('innerHTML'))

        # 循环文章列表
        for article in articleWebElementList:
            author = article.find_element_by_tag_name("h2").text
            content = article.find_element_by_tag_name("span").text
            sqlArg = [author, content]
            self.sqlArgs.append(sqlArg)
        
        next_page = self.driver.find_element_by_xpath("//*[@id='content-left']/ul/li[last()]/a")
        next_page.click()
        time.sleep(1)
        if self.page < 5:
            print('fetching page no-',self.page)
            self.parse()
        else:
            
            print('fetching page done')
    
    # 保存到数据库
    def saveToDB(self):
        sql = 'insert into article(author,content) values("%s","%s")'
        dbHandle = DataBaseHandle('192.168.10.202', 'root', 'root', 'selenium', 3306)
        dbHandle.insertManyDB(sql, self.sqlArgs) 
        dbHandle.closeDB()


if __name__== '__main__':
    spider = QsbkSpider()
    # fetching a page
    spider.driver.get('http://www.qiushibaike.com/text/')
    print("start the spider")
    spider.parse()
    spider.saveToDB()
    # print('total numer:',len(spider.sqlArgs))
    # 关闭浏览器
    spider.driver.close()

