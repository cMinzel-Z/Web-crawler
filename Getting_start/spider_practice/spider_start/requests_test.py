# -*- coding: utf-8 -*-

import requests
#import json

#res = requests.get("http://www.baidu.com")
#print(res.text)
#requests.post()
#requests.put()
#requests.options()
#requests.patch()
#requests.delete()

url = "http://127.0.0.1:8000"
params = {
        "username":"bobby",
        "password":"bobby"
        }

#res = requests.get("http://127.0.0.1:8000", params = params)
# data 和 json参数都可以传递 字符串 或 dict
#res = requests.post(url, data = json.dumps(params))
#res = requests.post(url, json = json.dumps(params))
res = requests.post(url, json = params)
#print(res.text)

#res = requests.get("http://www.baidu.com")
#print(res.encoding)
#
#res = requests.get("http://www.taobao.com")
#print(res.encoding)
#
#print(res.status_code)

#my_headers = {
#        "user-agent":"requests",
#        "imooc_uid":"321"
#        }
#res = requests.get(url, headers =my_headers)
#print(res.headers)
#
#res_b = requests.get("http://www.baidu.com")
#print(res_b.headers)
