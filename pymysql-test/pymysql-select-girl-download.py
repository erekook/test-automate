import urllib.request
import sys
from DataBaseHandle import *
import sys
import time
import random
import os
from tqdm import tqdm

'''
    查询数据库的图片url，并下载
'''

imgUrls = []
dir_path = '/home/erek/Pictures/goodsth'
my_headers = [
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
dbHandle = DataBaseHandle('192.168.10.200', 'root', 'root', 'selenium', 3306)

# 保存图片到本地
def saveImages():
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for index,img in enumerate(tqdm(imgUrls)):
        img_file_name = time.strftime('%Y%m%d%H%M%S') + str(index) + '.jpg'
        img_file_path = '%s/%s' % (dir_path, img_file_name)
        print(img_file_path)
        try:
            with open(img_file_path, 'wb') as handle:
                user_agent = random.choice(my_headers)
                header = {
                    'User-Agent': user_agent
                }
                req = urllib.request.Request(img, headers=header)
                res = urllib.request.urlopen(req).read()
                handle.write(res)
        finally:
            print('save successfully')


def getImgUrls():
    sql = 'select id,image from girl where download_flag = 0'
    # return type is tuple
    tupGirls = dbHandle.selectDB(sql)
    if len(tupGirls) == 0:
        print('没有找到数据')
        return

    for girl in tupGirls:
        imgUrls.append(girl[1]) # img url
        updateImgDownloadFlag(girl[0]) # img id

def updateImgDownloadFlag(id):
    sql = 'update girl set download_flag = 1 where id = ' + str(id)
    dbHandle.updateDB(sql)

if __name__ == '__main__':
    getImgUrls()
    saveImages()
    dbHandle.closeDB()
