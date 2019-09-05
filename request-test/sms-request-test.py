import requests
import threading
import time
import json

'''
    测试短信接口
'''
class smstest():
    
    def __init__(self):
        self.phone = "15952119656"
        self.url = "http://192.168.10.252:8091/web/api/smsLog/smsCode/"
        self.headers = {
            'content-type': 'application/json',
            'weId': '1',
            'X-Nideshop-Token': 'oM-3W5S_L6_4cl0cV7kFIC7l7icg4'
        }
        self.success = 0


    def get(self):
        try:
            print('request:', self.url + self.phone)
            r = requests.get(self.url + self.phone, headers=self.headers)
            res = json.loads(r.text)
            if res['code'] == '0':
                self.success += 1
            print(r.text)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    smsTest = smstest()
    try:
        i = 0
        # 线程数
        tasks_number = 10
        print('test begin')
        # 当前cpu时间
        time1 = time.clock()
        while i < tasks_number:
            t = threading.Thread(target=smsTest.get())
            t.start()
            i += 1
        time2 = time.clock()
        times = time2 - time1
        print('success times:',smsTest.success)
        print('cost time:',times)
    except Exception as e:
        print(e)
