#!/user/bin/python
# -*-coding:utf8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random
#from urllib import request
import urllib.request
import sys
sys.path.append('../pymysql-test/')
from DataBaseHandle import *

'''
    done:爬取图片,下载到本地
    todo:爬取图片链接存到数据库， 写个循环任务下载图片到本地
    problems: 1. 爬取的网站加载很慢，需要强制停止加载
              2. 图片是懒加载的，需要使用js来控制滚动条
'''
class WeiboSpider(object):

    def __init__(self):
        '''init data'''
        # 解决chrome在root下无法打开的问题
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        # 隐藏浏览器
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        # Create a new instance of the Chrome driver
        self.driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capa)
        self.wait = WebDriverWait(self.driver, 15)
        #self.driver.set_page_load_timeout(10)
        #self.driver.set_script_timeout(10)
        self.images = []
        self.dir_path = '/home/erek/Pictures/weibo'
        # 爬取总页数
        self.page = 1
        # 当前页数
        self.current = 0
        self.my_headers = [
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 " 
        ]

    # 爬取内容 
    def parse(self):
        #self.driver.get('https://www.aqk6.com/tupian/59946.html')
        self.current += 1
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "videopic")))
        self.driver.execute_script("window.stop() ? window.stop() : document.execCommand('Stop')")
        print('begin to parse')
        # 滚动滚动条
        self.driver.execute_script("window.scrollBy(0,2500)")
        for i in range(20):
            self.driver.execute_script("window.scrollBy(0,1000)")
            print('scroll time:', i)
            time.sleep(3)
        
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"videopic")))
        # 图片列表
        picClassList = self.driver.find_elements_by_class_name("videopic")
        next_page = self.driver.find_element_by_xpath("//*[@id='main-container']/div[5]/div[2]/a")
        print('fetching page:number %s | %s' % (self.current, self.driver.current_url))
        print('get the img list')
        for pic in picClassList:
            # url = pic.find_element(By.TAG_NAME, "img").get_attribute("src")
            url = pic.get_attribute("src")
            if url.find("default") == 0:
                continue
            image = [url, self.driver.current_url, next_page.text, '0']
            print(pic.get_attribute("src"))
            # print(pic.get_attribute("innerHTML"))
            self.images.append(image)

        # 进入下一页,跳转到新页面
        next_page.click()       
        time.sleep(2)
        # 关闭当前页面
        self.driver.close()
        # 获取当前全部页面句柄
        all_handles = self.driver.window_handles
        # 跳转到新页面的句柄
        self.driver.switch_to.window(all_handles[0])
        # 获取当前页面句柄
        #current_handle = self.driver.current_window_handle
        if self.current < self.page:
            self.parse()
        else:
            print(self.images)
            print('save to db')
            self.saveToDB()     



    # 保存到数据库
    def saveToDB(self):
        sql = 'insert into girl(image,url,title,download_flag) values("%s","%s","%s","%s")'
        dbHandle = DataBaseHandle('192.168.10.200', 'root', 'root', 'selenium', 3306)
        dbHandle.insertManyDB(sql, self.images) 
        dbHandle.closeDB()

    # 保存图片到本地
    def saveImages(self):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        for index,img in enumerate(self.imgUrls):
            img_file_name = time.strftime('%Y%m%d%H%M%S') + str(index) + '.jpg'
            img_file_path = '%s/%s' % (self.dir_path, img_file_name)
            print(img_file_path)
            try:
                with open(img_file_path, 'wb') as handle:
                    user_agent = random.choice(self.my_headers)
                    header = {
                        'User-Agent': user_agent
                    }
                    req = urllib.request.Request(img, headers=header)
                    res = urllib.request.urlopen(req).read()
                    handle.write(res)
            finally:
                print('save successfully')

if __name__ == '__main__':
    spider = WeiboSpider()
    # fetching a page
    #spider.driver.get('https://weibo.com/?category=10007')
    spider.driver.get('https://www.aqk6.com/tupian/59947.html')
    print("start the spider")
    spider.parse()
    #spider.saveImages()
    #spider.saveToDB()
    # 关闭浏览器
    spider.driver.close()

